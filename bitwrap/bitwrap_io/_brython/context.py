import json
from browser import window, document
from browser import ajax, console
from controller import Controller
from editor import Editor
from broker import Broker

class Context(object):
    """ application context object provides an interface to server-side api calls """

    def __init__(self):
        self.seq = 0
        self.endpoint = ''
        self.broker = Broker
        self.log = console.log
        self._get(window.Bitwrap.config, self.configure)
        self.doc = document

    def time(self):
        """ return time in microseconds """
        return window.Date.now()

    def configure(self, req):
        """ load config from server """
        _config = json.loads(req.text)
        self.endpoint = _config['endpoint']
        _editor = Editor(context=self, config=_config)

        if _config.get('use_websocket', False):
            self.broker(config=_config, editor=_editor)

        Controller(context=self, editor=_editor)

    @staticmethod
    def echo(req):
        """ write return value to consoel """
        try:
            txt = getattr(req, 'response')
            console.log(txt)
        except:
            console.log(req)

    @staticmethod
    def clear(txt=''):
        """ clear python terminal """
        document['code'].value = txt

    def upload_pnml(self, name, body, callback=None, errback=None):
        """  upload_pnml(filename, body, callback=None, errback=None): upload xml petri-net definition"""
        req = ajax.ajax()

        if callback:
            req.bind('complete', callback)
        else:
            req.bind('complete', self.echo)

        req.open('POST', self.endpoint + '/petrinet/' + name, True)
        req.set_header('content-type', 'application/xml')
        req.send(body)

    def _rpc(self, method, params=[], callback=None, errback=None):
        """  _rpc(method, params=[], callback=None, errback=None): make JSONRPC POST to backend """
        self.seq = self.seq + 1
        req = ajax.ajax()

        if callback:
            req.bind('complete', callback)
        else:
            req.bind('complete', self.echo)

        req.open('POST', self.endpoint + '/api', True)
        req.set_header('content-type', 'application/json')
        req.send(json.dumps({'id': self.seq, 'method': method, 'params': params}))

    def _get(self, resource, callback=None, errback=None):
        """ _get(resource, callback=None, errback=None): make http GET to backend """
        req = ajax.ajax()
        if callback:
            req.bind('complete', callback)
        else:
            req.bind('complete', self.echo)
        req.open('GET', self.endpoint + resource, True)
        req.send()

    def schemata(self, callback=None):
        """ schemata(callback=None): retrieve list of available state machine definitions """
        self._get('/schemata', callback=callback)

    def state(self, schema, oid, callback=None):
        """  state(schema, oid, callback=None): get current state """
        self._get('/state/%s/%s' % (schema, oid), callback=callback)

    def machine(self, schema, callback=None):
        """ machine(schema, callback=None): get machine definition """
        self._get('/machine/%s' % schema, callback=callback)

    def dispatch(self, schema, oid, action, payload={}, callback=None):
        """ dispatch(schema, oid, action, payload={}): dispatch new event to socketio  """
        if self.broker.socket:
            self.broker.commit(schema, oid, action, payload=payload)
        else:
            self.commit(schema, oid, action, payload=payload, callback=callback)

    def commit(self, schema, oid, action, payload={}, callback=None):
        """ commit(schema, oid, action, payload={}, callback=None): post new event to api  """
        req = ajax.ajax()

        if callback:
            req.bind('complete', callback)
        else:
            req.bind('complete', self.echo)

        req.open('POST', self.endpoint + '/dispatch/%s/%s/%s' % (schema, oid, action), True)
        req.set_header('content-type', 'application/json')
        data = json.dumps(payload)
        req.send(str(data))


    def stream(self, schema, oid, callback=None):
        """ stream(schema, oid, callback=None): get all events """
        self._get('/stream/%s/%s' % (schema, oid), callback=callback)

    def event(self, schema, eventid, callback=None):
        """ event(schema, eventid, callback=None): get a single event """
        self._get('/event/%s/%s' % (schema, eventid), callback=callback)

    def exists(self, schema=None, oid=None, callback=None, errback=None):
        """ exists(schema=None, oid=None, callback=None, errback=None): test for existance of schema and/or stream """

        if not oid:
            self._rpc('schema_exists', params=[schema], callback=callback, errback=errback)
        else:
            self._rpc('stream_exists', params=[schema, oid], callback=callback, errback=errback)

    def load(self, machine_name, new_schema):
        """ load(machine_name, new_schema): load machine definition as db schema """
        self._rpc('schema_create', params=[machine_name, new_schema])

    def create(self, schema, oid):
        """ create(schema, oid): create a new stream """
        self._rpc('stream_create', params=[schema, oid])

    def destroy(self, schema, callback=None):
        """ destroy(schema, callback=None): drop from db / destroys a schema and all events """
        self._rpc('schema_destroy', params=[schema], callback=callback)
