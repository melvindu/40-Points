from sqlalchemy.exc import IntegrityError

import fortypoints as fp
from fortypoints.users.models import User
from fortypoints.users.exceptions import InvalidPasswordException

db = fp.db


def get_user(email, password):
  user = User.get(email=email)
  if user.check_password(password):
    return user
  else:
    raise InvalidPasswordException


def create_user(name, email, password):
  user = User(name, email, password)
  db.session.add(user)
  try:
    db.session.commit()
    return user
  except IntegrityError:
    db.session.rollback()
    
