import fortypoints as fp
from fortypoints.users.models import User 

db = fp.db

def get_user(**kwargs):
  return User.get(**kwargs)

def create_user(name, email, password):
  db.session.add(User(name, email, password))
  db.session.commit()