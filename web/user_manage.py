from tornado.gen import coroutine

from web import BaseHandler
from execute_sqls.current_sql import select_property_data, update_table_data, \
    insert_table_new_data
from lib.constant.common import USER_ERROR, REDIS_TIME, UPDATE_PASSWORD_ERROR, \
    INSERT_USER_ERROR, USER_NULL_ERROR, USER_REPEAT_ERROR
from lib.redis_db import RedisInstance
from utils.utils import create_md5


class HomeHandler(BaseHandler):
    @coroutine
    def get(self):
        user_name = self.redis.get(self.cookie_str)
        if not user_name:
            self.render('./login.html')
        else:
            self.render('./home.html', user_name=user_name)


class LoginHandler(BaseHandler):
    @coroutine
    def post(self):
        name = self.get_body_argument('user_name')
        password = self.get_body_argument('password')
        password = create_md5(password, self.md5_str)
        where_clause = ' name="{}" and password="{}"'.format(name, password)
        data = yield select_property_data('user', where_clause=where_clause)
        if not data:
            self.status = 1
            self.msg = USER_ERROR
        else:
            cookies = self.cookie_str
            self.redis.set(cookies, name)
            self.redis.expire(cookies, REDIS_TIME)
        self.build_json_response({}, self.status, self.msg)


class LogOutHandler(BaseHandler):
    @coroutine
    def get(self):
        cookies = self.cookie_str
        self.redis.expire(cookies, 0)
        self.render('./login.html')


class CreateUserHandler(BaseHandler):
    @coroutine
    def post(self):
        user_name = self.get_body_argument('user_name')
        password = self.get_body_argument('password')
        if not user_name or not password:
            self.status = 1
            self.msg = USER_NULL_ERROR
            self.build_json_response({}, self.status, self.msg)

        db_user = yield select_property_data('user', 'name', user_name)
        if db_user:
            self.status = 1
            self.msg = USER_REPEAT_ERROR
        if self.status == 0:
            password = create_md5(password, self.md5_str)
            insert_data = dict(
                name=user_name, password=password
            )
            ret = yield insert_table_new_data('user', insert_data)
            if not ret:
                self.status = 1
                self.msg = INSERT_USER_ERROR
        self.build_json_response({}, self.status, self.msg)


class PasswordEditHandler(BaseHandler):
    @coroutine
    def post(self):
        user_id = self.get_body_argument('id')
        password = self.get_body_argument('password')
        password = create_md5(password, self.md5_str)
        update_data = dict(password=password)
        ret = yield update_table_data('user', update_data, user_id)
        if not ret:
            self.status = 1
            self.msg = UPDATE_PASSWORD_ERROR
        self.build_json_response({}, self.status, self.msg)
