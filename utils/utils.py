import base64
import os
import random
import re
import string
import traceback
import uuid
import json
import socket
import struct
import datetime
import logging
import urllib
import hashlib
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import six

bytes_type = six.binary_type
unicode_type = six.text_type
basestring_type = six.binary_type

_UTF8_TYPES = (bytes_type, type(None))
_TO_UNICODE_TYPES = (unicode_type, type(None))
HERE = os.path.realpath(os.path.dirname(__file__))


def utf8(text):
    """
        Converts a string argument to a byte string.

        If the argument is already a byte string or None, it is returned unchanged.
        Otherwise it must be a unicode string and is encoded as utf8.
    """
    if isinstance(text, _UTF8_TYPES):
        return text
    assert isinstance(text, unicode_type), \
        "Expected bytes, unicode, or None; got %r" % type(text)
    return text.encode("utf-8")


def to_unicode(text):
    """
        Converts a string argument to a unicode string.

        If the argument is already a unicode string or None, it is returned
        unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(text, _TO_UNICODE_TYPES):
        return text
    assert isinstance(text, bytes_type), \
        "Expected bytes, unicode, or None; got %r" % type(text)
    return text.decode("utf-8", 'ignore')


channel_re = re.compile(r'[a-z0-9]')
phone_re = re.compile(r'[0-9]{11}')
# check_phone_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
check_phone_re = re.compile('^1\d{10}$')


def is_valid_channel_name(channel):
    return channel_re.match(channel)


def is_valid_phone(phone):
    return phone_re.match(phone)


def check_phone(phone):
    phone = str(phone).split('.')[0]
    phone_match = check_phone_re.match(phone)
    if phone_match:
        return True
    else:
        return False


def gen_order_no():
    return uuid.uuid1()


def get_random_str(num=15):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num))


def fill_zero(data, max_length=10):
    data = str(int(data))
    zero_num = max_length - len(data)
    if zero_num >= 1:
        return '0' * zero_num + str(data)
    return data


def format_thousand_int(source, add_symbol=False):
    """
    格式化数字，间隔三个出一个逗号
    第一种方法   "{:,}".format(source)
    第二种方法   re.sub(r"(?<=\d)(?=(?:\d\d\d)+$)", ",", source)
    :param source:
    :param add_symbol:
    :return:
    """
    result = "{:,}".format(source)
    if add_symbol:
        source = int(source)
        if source > 0:
            result = '+{}'.format(result)
    return result


def replace_html_tag(content):
    return re.sub('<[^>]*?>', '', content)


def remove_emoj(text):
    text = to_unicode(text)
    re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
    filtered_string = re_pattern.sub(u'', text)
    filtered_string = utf8(filtered_string)
    return filtered_string


def url_encode_dict(target_dict):
    encode_list = []
    for k, v in target_dict.items():
        if not isinstance(v, (str, unicode_type)):
            v = str(v)
        encode_list.append('{}={}'.format(k, urllib.quote(v)))
    return '&'.join(encode_list)


def safe_int(value, default=0):
    try:
        value = int(value)
    except:
        value = default
    return value


def safe_log(log_obj, log_msg, level='info'):
    try:
        func = getattr(log_obj, level)
        func(log_msg)
    except:
        print(traceback.format_exc())


class FancyDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)


def is_valid_public_ip(ip):
    """
    是否是有效的公网IP
    :param ip:
    :return: 是否有效 True/False
    """
    ip = ip.strip() if ip else ''
    if not ip:
        logging.info('[is_valid_public_ip]error ip:{}'.format(ip))
        return False
    if ip == '127.0.0.1':
        logging.info('[is_valid_public_ip]error ip:{}'.format(ip))
        return False
    if ip.startswith('10.'):
        logging.info('[is_valid_public_ip]error ip:{}'.format(ip))
        return False
    if ip.startswith('192.168.'):
        logging.info('[is_valid_public_ip]error ip:{}'.format(ip))
        return False
    for i in range(16, 32):
        if ip.startswith('172.{}.'.format(i)):
            logging.info('[is_valid_public_ip]error ip:{}'.format(ip))
            return False
    return True


def ip_to_ip_num(ip):
    """
    ip转换为ip对应的数字，例如
    '101.226.103.0/25' -> 1709336320
    :param ip:
    :return:
    """
    return int(socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0]))


def ip_num_to_ip(ip_num):
    """
    ip对应的数字转换为ip
    1709336320 -> '101.226.103.0/25'
    :param ip_num:
    :return:
    """
    return socket.inet_ntoa(struct.pack('I', socket.htonl(ip_num)))


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, datetime.timedelta):
            return obj.total_seconds()
        if isinstance(obj, set):
            return list(obj)
        return super(JsonEncoder, self).default(obj)


def mask_name(raw_name):
    """
    给名字打"*"
    :param raw_name:
    :return:
    """
    if not raw_name:
        return ''

    name = raw_name[0] + '*' * (len(raw_name) - 1)
    return name


def mask_phone(raw_phone):
    """
    给名字打"*"
    :param raw_phone:
    :return:
    """
    if not raw_phone:
        return ''
    try:
        length = len(raw_phone)
        raw_phone = raw_phone[0:3] + '*' * (len(raw_phone) - 7) + raw_phone[length - 4:length]
        return raw_phone
    except Exception as e:
        logging.error(e)
        return raw_phone


def remove_same_item(target_list):
    end_list = []
    for item in target_list:
        if item not in end_list:
            end_list.append(item)
    logging.info('[remove_same_item]target_list:{}, end_list:{}'.format(target_list, end_list))
    return end_list


def mask_id_no(raw_id_no):
    """
    给名字打"*"
    :param raw_id_no:
    :return:
    """
    if not raw_id_no:
        return ''
    try:
        length = len(raw_id_no)
        raw_id_no = raw_id_no[0:3] + '*' * (length - 7) + raw_id_no[length - 4:length]
        return raw_id_no
    except Exception as e:
        logging.error(e)
        return raw_id_no


def send_email(receiver, title, body, file_path=None):
    if file_path:
        send_email_file(receiver, title, body, file_path)
    else:
        host = 'smtp.mxhichina.com'
        sender = 'report@heiniubao.com'
        pwd = 'Heiniu1003'
        msg = MIMEText(body, 'html', 'utf-8')
        msg['subject'] = title
        msg['from'] = sender
        if isinstance(receiver, list):
            msg['to'] = ",".join(receiver)
            # print msg
        else:
            msg['to'] = receiver
            # print msg
        s = smtplib.SMTP(host, port=80)
        # s.starttls()
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())
        s.quit()
        s.close()


def send_email_file(receiver, title, body, file_path):
    host = 'smtp.mxhichina.com'
    sender = 'report@heiniubao.com'
    pwd = 'Heiniu1003'

    part = MIMEApplication(open(file_path, 'rb').read())
    file_name = '客户管理日报{}'.format(file_path.split('/')[-1])
    part.add_header('Content-Disposition', 'attachment',
                    filename=file_name)  # 发送文件名称
    # MIMEMultipart对象代表邮件本身
    msg = MIMEMultipart()
    msg.attach(part)
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    msg['subject'] = title
    msg['from'] = sender
    if isinstance(receiver, list):
        msg['to'] = ",".join(receiver)
        # print msg
    else:
        msg['to'] = receiver
        # print msg
    s = smtplib.SMTP(host, port=80)
    # s.starttls()
    s.login(sender, pwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()
    s.close()


def add_extension_url_arg(url, name, value):
    if '?' in url:
        separator = '&'
    else:
        separator = '?'
    try:
        value_quote = urllib.quote(value)
    except:
        value_quote = ''
    url = '{url}{separator}{name}={value}'.format(
        url=url, separator=separator, name=name, value=value_quote
    )
    return url


def add_extension_url_arg_extend(url, update_dict, insert=False, use_quote=True):
    url_base = url.split('?')[0]
    arg_dict = {}
    for item in url.split('?')[-1].split('&'):
        if len(item.split('=')) != 2:
            continue
        name, value = item.split('=')
        arg_dict[name] = value

    args_list = []
    for k, v in update_dict.items():
        if use_quote:
            try:
                value_quote = urllib.quote(utf8(v))
            except:
                value_quote = ''
        else:
            value_quote = v
        if k not in arg_dict:
            if insert:
                arg_dict[k] = value_quote
        else:
            arg_dict[k] = value_quote
    for k, v in arg_dict.items():
        line = '{}={}'.format(k, v)
        args_list.append(line)

    url = '{url_base}?{args_str}'.format(
        url_base=url_base, args_str="&".join(args_list)
    )
    return url


def add_all_extension_url_arg(url, arg_dict=dict()):
    for name, value in arg_dict.items():
        if value is not None and value != '':
            url = add_extension_url_arg(url, name, value)
    return url


def remove_ascii_hidden_character(content):
    content = re.sub('[\x00-\x1F]', '', content)
    return content


def md5_value(content):
    content = to_unicode(content)
    return hashlib.md5(content.encode('utf-8')).hexdigest().upper()


def create_md5(pwd, salt):

    md5_obj = hashlib.md5(salt.encode('utf-8'))
    md5_obj.update(pwd.encode('utf-8'))
    return md5_obj.hexdigest()


def get_post_array_field_value(form_dict, field_name, default=None):
    """
    从post的form表单中，专门获取数组类型字段的数据
    :param form_dict: form表单
    :param field_name: 字段
    :param default: 没有此字段时，返回的默认值
    :return:
    """
    data_dict = {}
    has_field = False
    for key, value in form_dict.items():
        starts_str = '{}['.format(field_name)
        if key.startswith(starts_str) and key.endswith(']'):
            has_field = True
            new_key = key.split(starts_str)[-1][:-1]
            data_dict[int(new_key)] = value[0]
    if not has_field:
        return default
    keys = sorted(data_dict.keys(), key=lambda x: x)
    result = [data_dict[k] for k in keys]
    return result


def get_post_dict_field_value(data_dict, field_name):
    """
    获取多重列表传输
    :param data_dict: request.form
    :param field_name: 字段名
    :return:
    """
    form_dict = data_dict
    from collections import defaultdict
    result__list = []
    result_dict = defaultdict(dict)
    for k, v in form_dict.items():
        starts = '{}['.format(field_name)
        if not k.startswith(starts):
            continue
        new_key = k.replace(starts, '')
        new_key_list = [item.replace(']', '') for item in new_key.split('[')]
        parent_dict = None
        end_index = len(new_key_list)
        for index, small_key in enumerate(new_key_list):
            if index == 0:
                parent_dict = result_dict
            if small_key not in parent_dict:
                parent_dict[small_key] = defaultdict(dict)
            if index == end_index - 1:
                # print 'end'
                parent_dict[small_key] = v[0]
            parent_dict = parent_dict[small_key]
            result__list.append(json.dumps(result_dict))
    return result__list[-1]


# def get_post_dict_field_value(form_dict, default=None):
#     data_dict = {}
#     data_list = []
#
#     one_id_list = []
#     for key, values in form_dict.items():
#         if re.findall(r'.*[\d+][id]', key):
#             one_index = re.findall(r'.*[(\d+)][id]', key)
#             one_id_list.append((one_index, values))
#
#     tow_id_list = []
#     for one_id in one_id_list:
#         for key, values in form_dict.items():
#             if re.findall(r'.*[{}][value][\d+][id]'.format(one_id[0]), key):
#                 tow_index = re.findall(r'.*[{}][value][(\d+)][id]'.format(one_id[0]), key)
#                 tow_id_list.append(tow_index, values)
#
#         operate_list = []
#         row_list = []
#         for tow_id in tow_id_list:
#             for key, value in form_dict.items():
#                 if re.findall(r'.*[{}][values][{}][value][\d+][id]'.format(
#                         one_id[0], tow_id[0]), key):
#
#                     operate_list.append(value)
#                 tow_id_operate_dict = dict(id=tow_id[1], value=operate_list)
#                 row_list.append(tow_id_operate_dict)
#         data_dict['id'] = one_id[1]
#
#         data_list.append(data_dict)
#     return data_list








class MysqlInstance(object):
    @staticmethod
    def _parse_sql(param_dict):
        key_list = ''
        value_list = ''
        for key in param_dict:
            value = param_dict[key]
            if value != None:
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


# 根据时间生产文件名
def create_filed_name(file_type):
    filed_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + str(file_type)
    return filed_name


# 根据保险公司生成文件名
def create_company_filed_name(companyname, type, file_type):
    filed_name = str(companyname) + '-' + str(type) + str(file_type)
    return filed_name


# 拼接参数
def splice_parameter(request, info, sub='', chan=''):
    user_cookie = request.cookies.get('session')
    user_id = request['session'].get(user_cookie)
    new_str = dict(user_id=user_id, info=info)
    new_str = json.dumps(new_str)
    return new_str


# 根据生日算age
def get_age(birth):
    age = 0
    try:
        date_time = datetime.datetime.strptime(birth, '%Y-%m-%d')
        current_time = datetime.datetime.now()
        age = current_time.year - date_time.year
        if current_time.month < date_time.month:
            age -= 1
        elif current_time.month == date_time.month and current_time.day < date_time.day:
            age -= 1
        return age
    except Exception:
        logging.info('birth:%s type is not valid' % birth)
    return age


# 20190801-20190902换成2019-08-01，2019-08-02
def get_two_date(st):
    start_data, end_data = st.split('-')
    start_data = start_data[:4] + '-' + start_data[4:6] + '-' + start_data[6:]
    end_data = end_data[:4] + '-' + end_data[4:6] + '-' + end_data[6:]
    return start_data, end_data


# '2019-08-01'，'2019-08-02' --》20190801-20190902
def get_two_datetime(st1, st2):
    st1 = str(st1.replace('-', ''))
    st2 = str(st2.replace('-', ''))
    return st1 + '-' + st2


if __name__ == '__main__':
    # a = '中国'
    # c = '中国'
    #
    # d = utf8(a)
    # e = utf8(c)
    # print(d, type(d))
    # print(e, type(e))
    # a = '1dfgdsf'
    # b = '1234'
    # c = create_md5(a, b)
    # print(c)
    print(AESUtil().encryt('123', 'jud12343fgt56786'))
    print(AESUtil().decrypt('Y/quK8EZL37UYlXHNGfFFA==', 'jud12343fgt56786')
    )