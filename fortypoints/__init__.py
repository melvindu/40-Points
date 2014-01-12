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
  from fortypoints.players.views import player as players_view
  from chat.views import chat as chats_view
  app.register_blueprint(users_view)
  app.register_blueprint(games_view, url_prefix='/game')
  app.register_blueprint(players_view, url_prefix='/player')
  app.register_blueprint(chats_view, url_prefix='/chat')

  if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler('fortypoints.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

  return app

app = create_app()

from fortypoints import jinja_filters

@app.route('/')
def index():
	return redirect(url_for('users.index'))
