from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordordField, BooleanField
from wtforms.fields import FieldList
from wtforms.validators import Required, EqualTo, Email

class NewGameForm(Form):
  players = FieldList(TextField('User'))