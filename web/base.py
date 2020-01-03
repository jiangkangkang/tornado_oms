from tornado.web import RequestHandler
from tornado.web import authenticated
from tornado.gen import coroutine

from lib.redis_db import RedisInstance


class BaseHandler(RequestHandler):
    def initialize(self):
        self.status = 0
        self.msg = ''
        self.md5_str = 'tornado_mos'
        self.cookie_str = str(self.request.cookies)
        self.redis = RedisInstance.instance().redis

    def get_current_user(self):
        user_name = self.redis.get(self.cookie_str)
        if user_name:
            return True
        else:
            return False

    @authenticated
    @coroutine
    def get(self):
        pass

    @authenticated
    @coroutine
    def post(self):
        pass

    def build_json_response(self, data, status=0, msg=''):
        result_dict = {
            "status": status,
            "msg": msg,
            "data": data
        }
        self.write(result_dict)


