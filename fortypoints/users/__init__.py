import hashlib
import random

from sqlalchemy.exc import IntegrityError

import fortypoints as fp
from fortypoints.users.models import User
from fortypoints.users.exceptions import InvalidPasswordException

db = fp.db

user_salts = {}
user_keys = {}

def get_user(**kwargs):
  return User.get(**kwargs)


def get_user_by_id(userid):
  return User.get(id=userid)


def create_user(name, email, password):
  user = User(name, email, password)
  db.session.add(user)
  try:
    db.session.commit()
    return user
  except IntegrityError:
    db.session.rollback()


def ghetto_user_key(username, salt):
  return hashlib.md5('{salt}{user}'.format(salt=str(salt), user=username)).hexdigest()

def ghetto_login_user(user):
  salt = random.getrandbits(128)
  user_salts[user.name] = salt
  user_key = ghetto_user_key(user.name, salt)
  user_keys[user_key] = user.name

def ghetto_logout_user(user):
  salt = user_salts[user.name]
  user_key = ghetto_user_key(user.name, salt)
  del user_salts[user.name]
  del user_keys[user_key]

def ghetto_is_logged_in(username, userkey):
  if username in user_salts:
    if userkey in user_keys.values():
      return True
  return False

def ghetto_get_user_key(username):
  return user