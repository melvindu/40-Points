from fortypoints import login_manager

@login_manager.unauthorized_handler
@templated('')
def handle_unauthorized():
  return 