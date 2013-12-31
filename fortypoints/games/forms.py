from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, SubmitField
from wtforms.fields import FieldList
from wtforms.validators import Required, EqualTo, Email

class NewGameForm(Form):
  players = FieldList(TextField('User'), min_entries=3)
  add_player = SubmitField()