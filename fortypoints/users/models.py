from fortypoints import db
from fortypoints.models import ModelMixin
from fortypoints.users import constants as USER

class User(db.Model, ModelMixin):
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


      def get_status(self):
        return USER.STATUS[self.status]

      def get_role(self):
        return USER.ROLE[self.role]

      def __repr__(self):
        return '<User {name}>'.format(name=self.name)