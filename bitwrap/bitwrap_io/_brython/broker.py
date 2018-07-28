from browser import window, console

class Broker(object):

    socket = None

    def __init__(self, config=None, editor=None):
        Broker.socket = window.io.connect('')
        Broker.socket.on('commit', editor.on_commit)

    @staticmethod
    def commit(schema, oid, action, payload=None):
        if not payload:
            payload = {}

        Broker.socket.emit(
            'dispatch',
            {'schema': schema, 'oid': oid, 'action': action, 'payload': payload}
        )
