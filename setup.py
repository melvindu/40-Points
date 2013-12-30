import fortypoints as fp

fp.create_app().test_request_context().push()
fp.db.create_all()

