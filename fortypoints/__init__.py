import os

from flask import Flask, g, session

from config import secret_key

app = Flask(__name__)
app.secret_key = secret_key

@app.route('/')
def index():
	return 'Forty Points'
