#!/usr/bin/env python

from livereload import Server

import bitwrap_io.server
from bitwrap_io.api import Config
from bitwrap_io.server import app, pnml_editor

# run livereload for brython development
if __name__ == '__main__':
    pnml_editor(app)

    # livereload is not compatible with socketio
    # so disable websocket usage
    Config.use_websocket = False

    server = Server(app.wsgi_app)
    server.watch('./bitwrap_io/_brython/')
    server.serve(port=8080)
