import logging

from tornado import gen

from lib.mysql_db import MysqlInstance


@gen.coroutine
def update_table_data(table, data_dict, id,
                            where_clause=None):
    """
    :param table:
    :param data_dict: 要更新的字段内容，字典形式
    :param id:
    :return:
    """
    sql = MysqlInstance.gen_update_sql(table, data_dict, id, where_clause)
    args = ()

    result = yield MysqlInstance().execute(sql, args)
    if result or result == 0:
        return True
    else:
        return False


# 单表属性查询
@gen.coroutine
def select_property_data(table, property=None, data=None, where_clause=None):
    """
    :param table:
    :param property: 查询的字段
    :param data: 查询内容
    :return:
    """
    if where_clause:
        where_sql = 'where ' + where_clause
    else:
        where_sql = 'where {}="{}"'.format(property, data)
    sql = 'select * from {} {}'.format(table, where_sql)
    result = yield MysqlInstance().query_all(sql)
    return result


# 通用——创建数据
@gen.coroutine
def insert_table_new_data(table, data_dict):
    """
    :param table: 操作的表名
    :param data_dict: 创建数据信息
    :return:
    """
    sql = MysqlInstance.gen_insert_sql(table, data_dict)
    sql = sql.replace('%', '%%')
    args = ()
    try:
        result = yield MysqlInstance().execute(sql, args)
        logging.info('insert_table_channel sql:{},result:{}'.format(sql,
                                                                    result))
    except Exception as e:
        logging.info('创建数据error:{}'.format(e))
        return False
    return result
