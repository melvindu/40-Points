import logging
import os.path
import uuid

from flask import current_app, request
from flask.ext.login import current_user, login_required

import fortypoints as fp
from fortypoints import app
from fortypoints.request import flask_context, websocket
