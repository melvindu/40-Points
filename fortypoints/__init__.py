import os

from flask import Flask, g, redirect, url_for, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
  app = Flask(__name__)
  app.secret_key = SECRET_KEY
  app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
  db.init_app(app)
  login_manager.init_app(app)

  from fortypoints.users.views import user as users_view
  from fortypoints.games.views import game as games_view
  app.register_blueprint(users_view)
  app.register_blueprint(games_view, url_prefix='/game')

  return app

app = create_app()

from fortypoints.request import websocket
@websocket(app, '/websocket')
def handle_websocket(ws):

    print ws
    while True:
        message = ws.receive()
        if message is None:
            break
        else:
            message = json.loads(message)

            r  = "I have received this message from you : %s" % message
            r += "<br>Glad to be your webserver."
            ws.send(json.dumps({'output': r}))
            
@app.route('/')
def index():
	return redirect(url_for('users.index'))
