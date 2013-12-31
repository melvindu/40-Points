from sqlalchemy.exc import IntegrityError

import fortypoints as fp
from fortypoints.users.models import User
from fortypoints.users.exceptions import InvalidPasswordException

db = fp.db


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
    
