from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from config import config_info

from apps.handlers import handlers


if __name__ == '__main__':
    app = Application(handlers, **config_info['setting'])
    http_server = HTTPServer(app)
    http_server.listen(config_info['WEB_GLOBAL']['web_port'])
    http_server.start()
    IOLoop.current().start()
