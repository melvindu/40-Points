from flask import Blueprint, redirect, render_template, request, url_for
from flask.ext.login import login_required, login_user

from fortypoints import login_manager
from fortypoints.request import nocache
from fortypoints.template import templated
from fortypoints.users.forms import LoginForm, RegisterForm

@login_manager.user_loader
def load_user(userid):
    return fp.users.models.User.get(id=userid)

@login_manager.unauthorized_handler
def handle_unauthorized():
  return redirect(url_for('users.login'))

user = Blueprint('users', __name__, template_folder='templates/users')

@user.route('/')
@login_required
def index():
  return 'HI'

@user.route('/login')
@nocache
def login():
  """
  Login form
  """
  form = LoginForm(request.form)
  # make sure data are valid, but doesn't validate password is right
  if form.validate_on_submit():
    user = User.get(email=form.email.data)
    # we use werzeug to validate user's password
    if user and user.check_password(form.password.data):
      # the session can't be modified as it's signed, 
      # it's a safe place to store the user id
      login_user(user)
      return redirect(url_for('index'))
    flash('Wrong email or password', 'error-message')
  return render_template("users/login.html", form=form)
