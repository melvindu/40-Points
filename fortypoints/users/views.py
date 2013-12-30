from flask import Blueprint

from fortypoints import login_manager
from fortypoints.template import templated

@login_manager.user_loader
def load_user(userid):
    return fp.users.models.User.get(id=userid)

@login_manager.unauthorized_handler
@templated('')
def handle_unauthorized():
  return 

user = Blueprint('users', __name__, template_folder='templates/users')

@user.route('/login')
@templated()
def login():
  return
