import fortypoints as fp
from fortypoints.core import db

fp.create_app().test_request_context().push()
db.create_all()

