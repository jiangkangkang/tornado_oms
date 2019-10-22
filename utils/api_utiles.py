import base64
import csv
import os
import uuid

import requests
import torndb
import xlrd
import logging

from utils.utils import md5_value, create_filed_name, utf8


# 获取分页内容
def get_page_data(current_page, page_size, data_list):
    current_page = int(current_page)
    page_size = int(page_size)
    start_page = (current_page - 1) * page_size
    end_page = start_page + page_size
    data_list = data_list[start_page: end_page]
    return data_list


def requests_get(path, data_dict):
    result = requests.get(url=path, params=data_dict)
    return result


def requests_post(path, data_dict):
    result = requests.post(path, data_dict)
    return result


# 拼接redis 换成 key
def redis_str_key(interface, data_dict, user_id=None):
    if user_id:
        redis_key = str(user_id) + ':' + interface
    else:
        redis_key = interface
    for key, value in data_dict.items():
        if value:
            redis_key += ':' + str(value)
    if redis_key == interface:
        for key, value in data_dict.items():
            redis_key += ':' + str(key)
    return redis_key


def get_user_name_phone_str(request):
    cookie = request.cookies.get('session')
    user_name_cookie = '{}{}'.format('user_name', cookie)
    uer_phone_cookie = "{}{}".format('user_phone', cookie)
    user_name = request['session'].get(user_name_cookie)
    phone = request['session'].get(uer_phone_cookie)
    return "name:{} phone:{}".format(user_name, phone)


def bas64_uploads_img(request, bas64_str):
    img_format = bas64_str.split(';')[0].split('/')[-1]
    replace_str = "data:image/{};base64,".format(img_format)

    bas64_str = bas64_str.replace(replace_str, "")
    if len(bas64_str) % 3 == 1:
        bas64_str += "=="
    elif len(bas64_str) % 3 == 2:
        bas64_str += "="

    md5_result = md5_value(bas64_str)
    file_new_name = '{}.{}'.format(md5_result, img_format)
    parent_name = md5_result[:3]
    root_path = 'images'
    # 储存地址
    dir_path = os.path.abspath(os.path.dirname('./'))
    storage_file_url = dir_path + '/static/uploads/{}/{}/{}'.format(
        root_path, parent_name, file_new_name)
    parent_file_path = os.path.dirname(storage_file_url)
    if not os.path.exists(parent_file_path):
        os.makedirs(parent_file_path)
    file_url = '/static/uploads/{}/{}/{}'.format(
        root_path, parent_name, file_new_name
    )
    logging.info('file_exists:{}'.format(os.path.exists(storage_file_url)))
    if not os.path.exists(storage_file_url):
        with open(storage_file_url, 'wb') as f:
            f.write(base64.b64decode(bas64_str))
    file_url = request.scheme + '://' + request.host + file_url
    logging.info('file_url:{}'.format(file_url))
    return file_url


def read_excel(file_obj, file_type='contents', start_number=1):
    """
    :param file_obj:
    :param file_type:
    :param start_number: 读取开始行数
    :return: 这里读出的数值为浮点值，不是整数
    """
    logging.info('excel Name:{}'.format(file_obj.name))
    if file_type == 'contents':
        wb = xlrd.open_workbook(filename=None, file_contents=file_obj.body)
    else:
        wb = xlrd.open_workbook(file_obj)
    table = wb.sheets()[0]
    all_list = []
    row_len = table.nrows
    print(row_len)
    for i in range(start_number, row_len):
        row_val = table.row_values(i)
        all_list.append(row_val)
    return all_list


# 删除静态文件
def remove_static_file(file_path):
    file_path, file_name = os.path.split(file_path)
    if file_name.split('.')[-1] in ['json', 'js', 'css', 'html', 'py', 'vue',
                                    'ttf']:
        pass
    file_path = file_path.split('static')[-1]
    new_file_path = './static' + str(file_path) + '/'
    try:
        filed_list = os.listdir(new_file_path)
    except FileNotFoundError:
        return
    print(filed_list)
    for filed in filed_list:
        if filed == file_name:
            os.remove(new_file_path + filed)
            logging.info('remove file {}'.format(new_file_path + filed))


# 生成导出文件csv
def data_to_csv(data_list, heads=None, num=0):
    """
    :param data_list:
    :param heads:
    :param num:
    :return:
    """

    url_filed = './static/download/'
    filed_list = os.listdir(url_filed)
    for filed in filed_list:
        if str(filed).split('.')[-1] == 'csv':
            os.remove(url_filed + filed)

    filed_name = create_filed_name('.csv')
    filed_path = url_filed + filed_name

    with open(filed_path, 'w', newline='', encoding='utf-8-sig') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(heads)
        lin = []
        for data in data_list:
            lin.append(list(data.values())[num:])
        csv_write.writerows(lin)
    return url_filed + filed_name


def _retry_db_execute(func_run, db, sql_exp, is_query, use_logging,
                      *parameters, **kwparameters):
    retry_max_num = 1
    retry_num = 0
    result = None
    sql_id = str(uuid.uuid1())
    if not is_query and use_logging:
        info_msg = '[mysql_db]sql_exp:{},parameters:{},kwparameters:{}'
        info_msg = info_msg.format(utf8(sql_exp), parameters, kwparameters)
        info_msg = info_msg.replace(',parameters:(),kwparameters:{}', '')
        logging.info(info_msg)
    log_template = '[mysql_db]sql_id:{},retry_num:{} but still error:{}'
    while retry_num <= retry_max_num:
        try:
            result = func_run()
        except torndb.OperationalError as e:
            if retry_num == retry_max_num:
                logging.info(log_template.format(sql_id, retry_num, e))
                raise
        else:
            break
        finally:
            # cost_time = (datetime.datetime.now() - begin_time).total_seconds()
            # logging.info('[mysql_db]sql_id:{},finally run cost_time:{} s'.format(sql_id, cost_time))
            retry_num += 1
    return result

if __name__ == '__main__':
    pass
    # data_dict = dict(
    #     company='1',
    #     id=2,
    #     query='query'
    # )
    # user_id = 2
    # redis_key_str = redis_str_key('company', data_dict, user_id)
    # print(redis_key_str)
