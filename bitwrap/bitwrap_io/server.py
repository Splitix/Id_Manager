# -*- coding: utf-8 -*-
import os
import uuid

from flask import request, g, session, flash, redirect, url_for, render_template, send_from_directory

from flask_github import GitHub

from bitwrap_io.api import bitwrap_api, app, sio

app.config['GITHUB_CLIENT_ID'] = os.environ.get('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.environ.get('GITHUB_CLIENT_SECRET')
github = GitHub(app)

@app.route('/login')
def login():
    return github.authorize()

@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('editor')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    #user = User.query.filter_by(github_access_token=oauth_token).first()
    #if user is None:
    #    user = User(oauth_token)
        #db_session.add(user)

    #user.github_access_token = oauth_token
    #db_session.commit()
    return redirect(next_url)

def pnml_editor(app):
    """ add routes to host petri-net editor """

    app.static_url_path = ''
    app.template_folder = os.path.abspath(os.path.dirname(__file__) + '/../templates')
    bitwrap_api(app)
    brython_folder = os.path.abspath(os.path.dirname(__file__) + '/_brython')

    @app.route('/<path:path>')
    def send_brython(path):
        """ serve static brython files """
        return send_from_directory(brython_folder, path)

    @app.route('/')
    def index():
        return redirect(url_for('editor'))

    @app.route('/editor')
    def editor():
        return render_template('editor.html')

if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi
    import socketio

    pnml_editor(app)
    app.secret_key = str(uuid.uuid4())
    sioapp = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 8080)), sioapp)
