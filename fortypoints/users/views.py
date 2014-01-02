from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required, login_user, logout_user

from fortypoints import login_manager
from fortypoints.request import nocache
from fortypoints.template import templated
from fortypoints import users
from fortypoints.users.exceptions import InvalidPasswordException
from fortypoints.users.forms import LoginForm, RegisterForm

@login_manager.user_loader
def load_user(userid):
    return users.get_user_by_id(userid=userid)

@login_manager.unauthorized_handler
def handle_unauthorized():
  return redirect(url_for('users.login'))

user = Blueprint('users', __name__, template_folder='templates/users')


@user.route('/')
@login_required
def index():
  return render_template('users/index.html')


@user.route('/login', methods=['GET', 'POST'])
def login():
  """
  Login form
  """
  form = LoginForm(request.form)
  # make sure data are valid, but doesn't validate password is right
  if form.validate_on_submit():
    user = users.get_user(email=form.email.data)
    # we use werzeug to validate user's password
    if user and user.check_password(form.password.data):
      # the session can't be modified as it's signed, 
      # it's a safe place to store the user id
      login_user(user)
      users.ghetto_login_user(user)
      return redirect(url_for('index'))
    flash('Wrong email or password', 'danger')
  return render_template('users/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
  """
  Logout route
  """
  try:
    users.ghetto_logout(current_user)
  except Exception:
    pass
  logout_user()
  return redirect(url_for('users.login'))


@user.route('/register', methods=['GET', 'POST'])
def register():
  """
  Register form
  """
  form = RegisterForm(request.form)
  # make sure data are valid, but doesn't validate password is right
  if form.validate_on_submit():
    user = users.create_user(form.name.data, form.email.data, form.password.data)
    if not user:
      flash('User already exists', category='warning')
      return redirect(url_for('users.login'))
    login_user(user)
    users.ghetto_login_user(user)
    return redirect(url_for('index'))
  return render_template('users/register.html', form=form)
