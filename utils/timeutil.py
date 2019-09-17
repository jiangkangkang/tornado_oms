#!usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time
from datetime import datetime, timedelta

DAY_SECOND = 24 * 60 * 60


def time_to_string_for_before(date_time, use_ch_date_format=False):
    now_time = datetime.now()
    timedelta = now_time - date_time
    t_seconds = timedelta.days * 24 * 3600 + timedelta.seconds

    if t_seconds < 60:
        if t_seconds < 0:
            t_result = date_time.strftime('%Y-%m-%d %H:%M:%S')
        elif t_seconds <= 10:
            t_result = u"刚刚"
        else:
            t_result = str(t_seconds / 10 * 10) + u"秒前"
    else:
        if t_seconds / 60 <= 60:
            t_result = str(t_seconds / 60) + u"分钟前"
        elif t_seconds / 60 / 60 < 24:
            t_result = str(t_seconds / 60 / 60) + u"小时前"
        else:
            if use_ch_date_format:
                t_result = u'{0}年{1}月{2}日'.format(
                    date_time.year, date_time.month, date_time.day
                )
            else:
                t_result = date_time.strftime('%Y-%m-%d')
    return t_result


def str_time_string_for_before(str_time):
    date_time = str_time_to_datetime(str_time)
    return time_to_string_for_before(date_time)


def timestamp_to_string_for_before(timestamp):
    date_time = get_date_time_from_timestamp(timestamp)
    return time_to_string_for_before(date_time)


def is_leap_year(year_num):
    if year_num % 100 == 0:
        if year_num % 400 == 0:
            return True
        else:
            return False
    else:
        if year_num % 4 == 0:
            return True
        else:
            return False


def str_time_to_datetime(str_time, format_str='%Y-%m-%d %H:%M:%S'):
    if isinstance(str_time, datetime):
        return str_time
    if format_str.startswith('%Y-%m-%d'):
        year, month, day = str_time.split(' ')[0].split('-')
        year = int(year)
        month = int(month)
        day = int(day)
        if day == 31 and month in (4, 6, 9, 11):
            day = 30
        if day > 28 and month == 2:
            day = 29 if is_leap_year(year) else 28
        if day < 10:
            day = '0{}'.format(day)
        if month < 10:
            month = '0{}'.format(month)
        new_day_str_time = '{}-{}-{}'.format(year, month, day)
        str_time = re.sub('\d{4}\-\d+\-\d{2}', new_day_str_time, str_time)
    dt = datetime.strptime(str_time, format_str)
    return dt


def datetime_to_str_time(date, format_str='%Y-%m-%d %H:%M:%S'):
    if not isinstance(date, datetime):
       return date
    return date.strftime(format_str)


def get_now_str(format_str='%Y-%m-%d %H:%M:%S'):
    return datetime.now().strftime(format_str)


def get_now_str_ymd(format_str='%Y-%m-%d'):
    return datetime.now().strftime(format_str)


def get_now_str_hms(format_str='%H:%M:%S'):
    return datetime.now().strftime(format_str)


def get_now():
    return datetime.now()


def get_timestamp(date_time=None):
    if not date_time:
        date_time = datetime.now()
    return int(time.mktime(date_time.timetuple()))


def get_date_time_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp)


def get_hour():
    return datetime.now().strftime('%H')


def to_tomorrow_second():
    return 86400 - (int(time.time()) - time.timezone) % 86400


def get_today_str(only_date=False):
    if only_date:
        return get_now_str()[:10]
    return get_now_str()[:10] + ' 00:00:00'


def get_date_time_delta(date_time, days=0, hours=0, minutes=0,
                        seconds=0):
    return date_time + timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds
    )


def get_today_zero_datetime():
    today_zero_str = get_today_str()
    today_zero_datetime = str_time_to_datetime(today_zero_str)
    return today_zero_datetime


# def get_one_day_time_zone():
#     """
#     获取昨天凌晨到今天凌晨的时间戳列表：['2017-07-13 00:00:00', '2017-07-14 00:00:00']
#     :return: tuple[str]
#     """
#     today = datetime.now()
#     yesterday = today - timedelta(days=1)
#     today_format = today.strftime('%Y-%m-%d %H:%M:%S')[:11]+'00:00:00'
#     yesterday_format = yesterday.strftime('%Y-%m-%d %H:%M:%S')[:11]+'00:00:00'
#     zone = (yesterday_format, today_format)
#     return zone


def get_one_day_time_zone():
    """
    获取昨天凌晨到今天凌晨的时间戳列表：['2017-07-13 00:00:00', '2017-07-14 00:00:00']
    :return: tuple[str]
    """
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d 00:00:00'), datetime.now().strftime('%Y-%m-%d 00:00:00')


# def get_one_hour_time_zone():
#     """
#     获取前一小时的时间戳列表：['2017-07-17 10:00:00', '2017-07-17 09:00:00']
#     :return: tuple[str]
#     """
#     now = datetime.now()
#     one_hour_ago = now - timedelta(minutes=60)
#     now_format = now.strftime('%Y-%m-%d %H:%M:%S')[:13]+':00:00'
#     one_hour_ago_format = one_hour_ago.strftime('%Y-%m-%d %H:%M:%S')[:13]+':00:00'
#     zone = (one_hour_ago_format, now_format)
#     return zone


def get_one_hour_time_zone():
    """
    获取前一小时的时间戳列表：['2017-07-17 10:00:00', '2017-07-17 09:00:00']
    :return: tuple[str]
    """
    one_hour_ago = datetime.now() - timedelta(hours=1)
    return one_hour_ago.strftime('%Y-%m-%d %H:00:00'), datetime.now().strftime('%Y-%m-%d %H:00:00')


def get_yesterday_str(only_date=False):
    yesterday = get_now() + timedelta(days=-1)
    result = datetime_to_str_time(yesterday, '%Y-%m-%d 00:00:00')
    if only_date:
        return result[:10]
    else:
        return result


def date_to_today(date_str):
    """
    date_str:'2019-01-01'
    """
    date = date_str.split('-')
    date = datetime(int(date[0]), int(date[1]), int(date[2]))
    today = get_today_str().split('-')
    today = datetime(int(today[0]), int(today[1]), int(today[2]))
    result = today - date
    return result.days


def get_yesterday_datetime():
    return str_time_to_datetime(get_yesterday_str())


def get_last_hour_str():
    target_date_time = get_date_time_delta(get_now(), hours=-1)
    return datetime_to_str_time(target_date_time)


def get_date_list(start_date, end_date):
    # start_date和end_date转换成datetime对象
    start_date = str_time_to_datetime(start_date, '%Y-%m-%d')
    end_date = str_time_to_datetime(end_date, '%Y-%m-%d')
    now = get_now()
    target_end = now + timedelta(hours=1)

    # 循环start_date和end_date的差值，获取区间内所有的日期
    date_list = []
    temp_date = start_date
    while temp_date <= end_date:
        if temp_date > target_end:
            break
        date_list.append(temp_date.strftime("%Y-%m-%d"))
        temp_date += timedelta(days=1)
    return date_list


def get_last_days_last_minute(last_days, format_str='%Y-%m-%d 23:59:59'):
    date_list = []
    now = get_now()
    for before_day in range(1, last_days + 1):
        target_datetime = get_date_time_delta(now, days=-before_day)
        date_list.append(datetime_to_str_time(target_datetime, format_str))
    return date_list


def get_time_of_day(start_date, end_date):
    if start_date == end_date and start_date is not None:
        end_date = str(end_date) + ' 23:59:59'
    return start_date, str(end_date)


def getNowYearWeek():
    # 当前时间年第几周的计算
    timenow = datetime.now()
    NowYearWeek = timenow.isocalendar()
    return NowYearWeek


# 指定日期所在周的周一日期
def getDayInweekMonday(st='2018-11-29'):
    time = datetime.strptime(st, "%Y-%m-%d")
    week_num = time.weekday()
    Monday = time + timedelta(days=-week_num)
    Monday = str(Monday)[0:10]
    return Monday


def time_span(ts):
    ts = str_time_to_datetime(ts)
    delta = datetime.now() - ts
    if delta.days >= 365:
        return '%d年前' % (delta.days / 365)
    elif delta.days >= 30:
        return '%d个月前' % (delta.days / 30)
    elif delta.days > 0:
        return '%d天前' % delta.days
    elif delta.seconds < 60:
        return "%d秒前" % delta.seconds
    elif delta.seconds < 60 * 60:
        return "%d分钟前" % (delta.seconds / 60)
    else:
        return "%d小时前" % (delta.seconds / 60 / 60)


def time_year_mouth(st):
    '''
    :param st:'2019-08-01 00:00:07'
    :return:'201908'
    '''
    return str(st).split(' ')[0].replace('-', '')[:-2]


def parse_2_str_time_to_day_range(start_time, end_time):
    start_time = start_time.split(' ')[0]
    end_time = end_time.split(' ')[0]
    if not start_time:
        start_time = datetime.now().strftime('%Y-%m-%d')
    if not end_time:
        end_time = datetime.now().strftime('%Y-%m-%d')

    today = datetime.now()
    end = (today - datetime.strptime(start_time, '%Y-%m-%d')).days
    start = (today - datetime.strptime(end_time, '%Y-%m-%d')).days
    if start < 0 or start > end:
        start = 0
    if end < 0:
        end = 0
    return range(start, end + 1)


def get_between_day(begin_date, end_date):
    """

    :param begin_date: '2019-07-01'
    :param end_date: '2019-07-04'
    :return: ['2019-07-01', '2019-07-02', '2019-07-03', '2019-07-04']
    """
    date_list = []
    begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += timedelta(days=1)
    return date_list


def get_target_day_str(before_day):
    now = get_now()
    return get_date_time_delta(now, days=-before_day).strftime('%Y-%m-%d')


if __name__ == '__main__':
    # before_day = 0
    print(get_now_str_ymd())
    start_date = '2019-09-04 12:00:00'
    end_date = '2019-09-05 12:00:00'
    for before_day in parse_2_str_time_to_day_range(start_date, end_date):
        date = (datetime.now() - timedelta(
            days=before_day)).strftime('%Y-%m-%d')
        print(date)