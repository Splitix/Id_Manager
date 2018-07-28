"""
bitwrap_io

usage:

    import bitwrap_io
    m = bitwrap_io.open('counter')
    m(oid='foo', action='INC_0', payload={}) # dispatch an event

"""
import sys
import bitwrap_io.storage as psql
from bitwrap_io.config import options


class EventStore(object):
    """ bitwrap_io.EventStore """

    _store = {}
    """ eventstore object cache """

    def __init__(self, schema, **kwargs):
        self.schema = schema.__str__()
        self.storage = psql.Storage(self.schema, **kwargs)

    def __call__(self, **request):
        """ execute a transformation """
        return self.storage.commit(request)

def open(schema, **opts):
    """ open an evenstore by providing a schema name """

    if not opts:
        opts = options()

    if not schema in EventStore._store:
        EventStore._store[schema] = EventStore(schema, **opts)

    return EventStore._store[schema]
