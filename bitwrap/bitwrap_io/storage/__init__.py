"""
bitwrap_psql - provies stateful event storage using postgresql

"""

from string import Template
from contextlib import contextmanager

import psycopg2
from psycopg2 import sql

from bitwrap_io.storage.postgres import connect

class Storage(object):
    """ PGSQL Storage provider """

    _pool = {}
    """ storage pool """

    def __init__(self, schema, **kwargs):
        if schema in Storage._pool:
            self.db = Storage._pool[schema]
        else:
            self.db = Database(schema, kwargs)
            Storage._pool[schema] = self.db

    def commit(self, req):
        """ execute transition and persist to storage on success """

        if 'payload' not in req or not req['payload']:
            req['payload'] = '{}'

        _sql = sql.SQL("""
        INSERT INTO {schema}.events(oid, action, payload)
          VALUES(%s, %s, %s)
        RETURNING
          to_json((hash, oid, seq )::{schema}.event) as event;
        """).format(schema=sql.Identifier(self.db.schema))

        with self.db.cursor() as cur:

            try:
                cur.execute(_sql, [req['oid'], req['action'], req['payload']])
                res = cur.fetchone()
                return res[0]

            except psycopg2.IntegrityError:
                msg = 'INVALID_OUTPUT'
            except psycopg2.InternalError:
                msg = 'INVALID_INPUT'
            except psycopg2.ProgrammingError as ex:
                msg = str(ex).splitlines()[0]

            return {'oid': req['oid'], 'action': req['action'], '__err__': msg}


class Database(object):
    """ store """

    def __init__(self, schema, rds_config):
        self.pool = connect(**rds_config)
        self.schema = schema
        self.states = States(self)
        self.events = Events(self)

    @contextmanager
    def cursor(self):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            self.pool.putconn(conn)

    def schema_exists(self):
        """
        test that an event-machine schema exists
        """

        with self.cursor() as cur:
            cur.execute(sql.SQL("""
            SELECT exists(select tablename from pg_tables where schemaname = %s and tablename = 'states');
            """), [self.schema])
            res = cur.fetchone()[0]

        return res

    def stream_exists(self, oid):
        """
        test that a stream exists
        """
        with self.cursor() as cur:
            cur.execute(sql.SQL("""
            SELECT exists(select oid FROM {}.states where oid = %s);
            """).format(sql.Identifier(self.schema)), [oid])
            res = cur.fetchone()[0]

        return res

    def create_stream(self, oid):
        """ create a new stream if it doesn't exist """


        with self.cursor() as cur:
            cur.execute(sql.SQL("""
            INSERT into {}.states (oid) values (%s)
            """).format(sql.Identifier(self.schema)), [oid])

        return True

class States(object):
    """ Model """

    def __init__(self, db):
        self.database = db

    def fetch(self, oid):
        """ get event by eventid """

        _sql = sql.SQL("""
        SELECT
          to_json((ev.hash, st.oid, ev.action, st.rev, st.state, ev.payload, modified, created)::{schema}.current_state)
        FROM
          {schema}.states st
        LEFT JOIN
          {schema}.events ev ON ev.oid = st.oid AND ev.seq = st.rev
        WHERE
          st.oid = %s
        """).format(schema=sql.Identifier(self.database.schema))

        with self.database.cursor() as cur:
            cur.execute(_sql, [oid])
            res = cur.fetchone()[0]

        return res

class Events(object):
    """ Model """

    def __init__(self, db):
        self.database = db

    def fetch(self, key):
        """ get event by eventid """

        _sql = sql.SQL("""
        SELECT
            row_to_json((hash, oid, seq, action, payload, timestamp)::{schema}.event_payload)
        FROM
            {schema}.events
        WHERE
            hash = %s
        ORDER BY seq DESC
        """).format(schema=sql.Identifier(self.database.schema))

        with self.database.cursor() as cur:
            cur.execute(_sql, [key])
            res = cur.fetchone()[0]

        return res

    def fetchall(self, oid):

        _sql = sql.SQL("""
        SELECT
            row_to_json((hash, oid, seq, action, payload, timestamp)::{schema}.event_payload)
        FROM
            {schema}.events
        WHERE
            oid = %s
        ORDER BY seq DESC
        """).format(schema=sql.Identifier(self.database.schema))

        with self.database.cursor() as cur:
            cur.execute(_sql, [oid])
            res = cur.fetchall()

        return [row[0] for row in res]
