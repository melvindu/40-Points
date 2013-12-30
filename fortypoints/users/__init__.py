from fortypoints import login_manager
from fortypoints.users.models import User

@login_manager.user_loader
def load_user(userid):
    return User.get(id=userid)