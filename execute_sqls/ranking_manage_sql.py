from tornado.gen import coroutine
from lib.mysql_db import MysqlInstance


@coroutine
def get_top_ranking():
    sql = '''select * 
             from ranking_manage 
             order by click_num desc limit 10'''
    result = yield MysqlInstance().query_all(sql)
    if not result:
        return []
    for row in result:
        for key, val in row.items():
            if key == 'create_time':
                row[key] = str(row[key])
                break
    return result
