from fortypoints.users.models import User 

def get_user(**kwargs):
  return User.get(**kwargs)