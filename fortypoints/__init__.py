import os

from flask import Flask, g, session
from flask_sqlalchemy import SQLAlchemy

from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()


def create_app():
  app = Flask(__name__)
  app.secret_key = SECRET_KEY
  app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
  db.init_app(app)
  return app

app = create_app()


@app.route('/')
def index():
	return 'Forty Points'
