import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = frozenset(['melvinclanceydu@gmail.com'])
SECRET_KEY = '\xe3f\xa7\xa0.c\xebw\n\xdf@\x03(T\x17\x91\xbb\xbek\x9asC^\x87'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/fortypoints'
DATABASE_CONNECT_OPTIONS = {}
