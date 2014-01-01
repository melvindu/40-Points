from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from chat import ChatSocketHandler, ChatApplication
from fortypoints import app

application = WSGIContainer(app)
http_server = HTTPServer(application)
chat_server = HTTPServer(ChatApplication())

http_server.listen(5000)
chat_server.listen(8888)

IOLoop.instance().start()
