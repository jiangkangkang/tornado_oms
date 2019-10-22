import logging
import traceback

from config import config_info
import tornado.gen
import tormysql
from tormysql import DictCursor


class MysqlInstance(object):
    def __init__(self):
        self.config_instance = config_info['MYSQL']
        self.__pool = self.__gen_db_conn()

    def __gen_db_conn(self):
        pool = tormysql.ConnectionPool(
            max_connections=self.config_instance['maxsize'],
            debug_connection_used=self.config_instance['debug'],
            host=self.config_instance['host'],
            database=self.config_instance['db'],
            user=self.config_instance['user'],
            password=self.config_instance['password'],
            charset=self.config_instance['charset'])
        return pool

    @tornado.gen.coroutine
    def query_all(self, sql, args=None):
        datas = []
        with (yield self.__pool.Connection()) as conn:
            try:
                with conn.cursor(cursor_cls=DictCursor) as cursor:
                    logging.info(sql, args, cursor)
                    yield cursor.execute(sql, args)
                    datas = cursor.fetchall()
            except Exception as e:
                logging.error(traceback.format_exc())
                logging.error("Query error: %s", e.args)
            else:
                yield conn.commit()

        raise tornado.gen.Return(datas)

    @tornado.gen.coroutine
    def execute(self, sql, args=None):
        ret = None

        with (yield self.__pool.Connection()) as conn:
            try:
                with conn.cursor(cursor_cls=DictCursor) as cursor:
                    logging.info(sql, args, cursor)
                    ret = yield cursor.execute(sql, args)
            except Exception as e:
                logging.error(traceback.print_exc())
                logging.error("Query error: %s", e.args)
                yield conn.rollback()
            else:
                yield conn.commit()

        raise tornado.gen.Return(ret)

    @staticmethod
    def _parse_sql(param_dict):
        key_list = ''
        value_list = ''
        for key in param_dict:
            value = param_dict[key]
            if value is not None:
                key_list += '%s, ' % key
                if isinstance(value, str):
                    value = value.replace("'", '"')
                    value_list += "'%s', " % value
                elif isinstance(value, int):
                    value_list += "%d, " % value
                else:
                    value_list += "'%s', " % value

        if key_list != '':
            key_list = key_list[:-2]
        if value_list != '':
            value_list = value_list[:-2]
        return key_list, '(' + value_list + ')'

    @staticmethod
    def gen_insert_sql(table, param_dict, use_ignore=False):
        key_list, value_list = MysqlInstance._parse_sql(param_dict)
        if use_ignore:
            front = 'INSERT IGNORE INTO'
        else:
            front = 'INSERT INTO'
        sql = '%s %s (%s) VALUES %s' % (front, table, key_list, value_list)
        return sql

    @staticmethod
    def gen_update_sql(table, param_dict, update_row_id=None,
                       where_clause=None):

        sql_exp = "UPDATE %s SET " % table
        for key in param_dict:
            value = param_dict[key]
            if isinstance(value, str):
                value = value.replace("'", '"')
                sql_exp += "%s = '%s'," % (key, value)
            elif isinstance(value, int):
                sql_exp += "%s = %d," % (key, value)
            else:
                value = value.replace("'", '"')
                sql_exp += "%s = '%s'," % (key, value)
        sql_exp = sql_exp[:-1] + " "
        if update_row_id is not None:
            sql_exp += ' WHERE id = %d' % int(update_row_id)
        elif where_clause is not None:
            sql_exp += ' WHERE {}'.format(where_clause)
        return sql_exp

