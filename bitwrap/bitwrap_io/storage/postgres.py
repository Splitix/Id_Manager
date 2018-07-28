from contextlib import contextmanager
from string import Template
from psycopg2.pool import ThreadedConnectionPool
from psycopg2 import sql

TOKEN_MAX = 65536

def connect(**kwargs):
    """ create new connection pool """
    return ThreadedConnectionPool( 2, 20,
        host=kwargs['pg-host'],
        user=kwargs['pg-username'],
        dbname=kwargs['pg-database'],
        password=kwargs['pg-password'],
    )

    return dbpool

@contextmanager
def get_cursor(opts):
    """ cursor context helper """

    if 'pool' in opts:
        pool = kwargs.pop('pool')
    else:
        pool = connect(**opts)

    conn = pool.getconn()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    finally:
        pool.putconn(conn)
        pool.closeall()

def drop_schema(schema, **kwargs):
    """ drop db schema """

    with get_cursor(kwargs) as cur:
        cur.execute("DROP SCHEMA IF EXISTS %s CASCADE" % schema)

def create_schema(machine, **kwargs):
    """ use machine definition to create database schema """

    with get_cursor(kwargs) as cur:
        _create_schema(machine, kwargs, cursor=cur)

def _create_schema(machine, options, cursor=None):
    """ add a new schema to an existing db """
    schema = options.get('schema_name', machine.name)
    schema_identifier = sql.Identifier(schema)

    cursor.execute(sql.SQL("CREATE schema {}").format(sql.Identifier(schema)))
    
    cursor.execute(sql.SQL("""
    CREATE DOMAIN {}.token as smallint CHECK(VALUE >= 0 and VALUE <= %s)
    """).format(sql.Identifier(schema)), [TOKEN_MAX])

    num_places = len(machine.machine['state'])
    columns = [''] * num_places
    vector = [''] * num_places
    delta = [''] * num_places

    # KLUDGE move these field defs closer to the format statement where they are used
    for key, props  in  machine.net.places.items():
        i = props['offset']
        columns[i] = ' %s %s.token' % (key, schema)
        vector[i] = ' %s int4' % key
        delta[i] = " (state).%s + txn.%s" % (key, key)

    # KLUDGE using string substitution 
    cursor.execute("""
    CREATE TYPE %s.state as ( %s )
    """ % (schema, ','.join(columns)))

    # KLUDGE using string substitution 
    cursor.execute("""
    CREATE TYPE %s.vector as ( %s )
    """ % (schema, ','.join(vector)))

    cursor.execute(sql.SQL("""
    CREATE TYPE {}.event as (
      id varchar(32),
      oid varchar(255),
      rev int4
    )
    """).format(schema_identifier))

    cursor.execute(sql.SQL("""
    CREATE TYPE {}.event_payload as (
      id varchar(32),
      oid varchar(255),
      seq int4,
      action varchar(255),
      payload json,
      timestamp timestamp
    )
    """).format(sql.Identifier((schema))))

    cursor.execute(sql.SQL("""
    CREATE TYPE {}.current_state as (
      id varchar(32),
      oid varchar(255),
      action varchar(255),
      rev int4,
      state {}.state,
      payload json,
      modified timestamp,
      created timestamp
    )
    """).format(sql.Identifier(schema), sql.Identifier(schema)))

    initial_vector = machine.net.initial_vector()

    # KLUDGE: this seems to be a limitation of how default values are declared
    # this doesn't work when state vector has only one element
    # state %s.state DEFAULT (0), # FAILS
    # state %s.state DEFAULT (0,0), # WORKS
    if len(initial_vector) < 2:
        raise Exception('state vector must be an n-tuple where n >= 2')

    cursor.execute(sql.SQL("""
    CREATE TABLE {}.states (
      oid VARCHAR(256) PRIMARY KEY,
      rev int4 default 0,
      state {}.state DEFAULT %s::{}.state,
      created timestamp DEFAULT now(),
      modified timestamp DEFAULT now()
    );
    """).format(schema_identifier, schema_identifier, schema_identifier), [tuple(initial_vector)])

    cursor.execute(sql.SQL("""
    CREATE TABLE {}.transitions (
      action VARCHAR(255) PRIMARY KEY,
      vector {}.vector
    );
    """).format(schema_identifier, schema_identifier))

    for key, props  in  machine.net.transitions.items():
        cursor.execute(sql.SQL("""
        INSERT INTO {}.transitions values(%s, %s)
        """).format(schema_identifier), [key, tuple(props['delta'])])

    cursor.execute(sql.SQL("""
    CREATE TABLE {}.events (
      oid VARCHAR(255) REFERENCES {}.states(oid) ON DELETE CASCADE ON UPDATE CASCADE,
      seq SERIAL,
      action VARCHAR(255) NOT NULL,
      payload jsonb DEFAULT %s,
      hash VARCHAR(32) NOT NULL,
      timestamp timestamp DEFAULT NULL
    );
    """).format(schema_identifier, schema_identifier), ['{}'])

    cursor.execute(sql.SQL("""
    ALTER TABLE {}.events ADD CONSTRAINT oid_seq_pkey PRIMARY KEY (oid, seq);
    """).format(schema_identifier))

    cursor.execute(sql.SQL("""
    CREATE INDEX hash_idx on {}.events (hash);
    """).format(schema_identifier))


    # KLUDGE using string substitution 
    function_template = Template("""
    CREATE OR REPLACE FUNCTION ${name}.vclock() RETURNS TRIGGER
    AS $MARKER
        DECLARE
            txn ${name}.vector;
            revision int4;
        BEGIN
            SELECT
                (vector).* INTO STRICT txn
            FROM
                ${name}.transitions
            WHERE
                action = NEW.action;

            UPDATE
              ${name}.states set 
                state = ( ${delta} ),
                rev = rev + 1,
                modified = now()
            WHERE
              oid = NEW.oid
            RETURNING
              rev into STRICT revision;

            NEW.seq = revision;
            NEW.hash = md5(row_to_json(NEW)::TEXT);
            NEW.timestamp = now();

            RETURN NEW;
        END
    $MARKER LANGUAGE plpgsql""")
    
    fn_sql = function_template.substitute(
        MARKER='$$',
        name=schema,
        var1='$1',
        var2='$2',
        var3='$3',
        delta=','.join(delta)
    )

    cursor.execute(fn_sql)

    trigger_sql = """
    CREATE TRIGGER {}
    BEFORE INSERT on {}.events
      FOR EACH ROW EXECUTE PROCEDURE {}.vclock();
    """

    cursor.execute(sql.SQL(trigger_sql).format(
        sql.Identifier(schema + '_dispatch'), schema_identifier, schema_identifier)
    )
