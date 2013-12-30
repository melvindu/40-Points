from werkzeug.security import check_password_hash, generate_password_hash

import fortypoints as fp
from fortypoints.models import ModelMixin
from fortypoints.users import constants as USER

db = fp.db

class User(db.Model, ModelMixin):
  __tablename__ = 'user'
  id = db.Column(db.Integer(unsigned=True), primary_key=True)
  name = db.Column(db.String(50), unique=True)
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(120))
  role = db.Column(db.SmallInteger, default=USER.USER)
  status = db.Column(db.SmallInteger, default=USER.NEW)

  def __init__(self, name=None, email=None, password=None):
    self.name = name
    self.email = email
    self.password = password

  @property
  def games(self):
    return self.players.games
    
  def get_status(self):
    return USER.STATUS[self.status]

  def get_role(self):
    return USER.ROLE[self.role]

  def set_password(self, password):
        self.password = generate_password_hash(password)

  def check_password(self, password):
      return check_password_hash(self.password, password)

  def __repr__(self):
    return '<User {name}>'.format(name=self.name)