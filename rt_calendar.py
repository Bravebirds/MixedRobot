# -*- coding: utf-8 -*-
"""
Project: MrYu-Github
Creator: Weather_Pm2.5
Create time: 2019-10-28 11:58
Introduction: 获取节假日及万年历信息
官网：https://www.juhe.cn
"""
import datetime
import requests
Proxy = {
    "http": "http://127.0.0.1:12639",
    "https": "https://127.0.0.1:12639",
}

def get_rtcalendar(date=''):
    """
    获取指定日期的节假日及万年历信息
    http://v.juhe.cn/calendar/day?#指定日期的节假日及万年历信息
    :param data: str 日期 格式 yyyyMMdd
    :rtype str
    """
    appKey = "d3f2885b3dffe5ff3006954b84f74e67"
    date_ = date or datetime.datetime.now().strftime('%Y-%m-%-d')
    print('获取 {} 的日历...'.format(date_))
    try:
        url='http://v.juhe.cn/calendar/day?date={date}&key={appKey}'.format(date=date_,appKey=appKey)
        resp = requests.get(url=url,proxies=Proxy)
        print(resp.text)
        if resp.status_code == 200:
            content_dict = resp.json()
            if content_dict['reason'] == 'Success':
                data_dict = content_dict['result']['data']
                date = data_dict['date']
                weekday = data_dict['weekday']
                lunarYear = data_dict['lunarYear']
                # suit = data_dict['suit']
                # avoid = data_dict['avoid']
                desc =data_dict['desc']
                holiday =data_dict['holiday']
                if weekday!='星期六' or weekday !='周日':
                    return_text = '{date}农历{lunarYear} {weekday} {holiday} {desc}'.format(date=date,weekday=weekday,desc=desc,holiday=holiday,lunarYear=lunarYear)
                else:
                    pass
                return return_text
            else:
                print('获取日历失败error_code:{}'.format(content_dict['error_code']))
                return None
        print('获取日历失败')
    except Exception as exception:
        print(str(exception))
    return None

if __name__ == '__main__':
    get_calendar = get_rtcalendar(date='2020-5-1')
    print(get_calendar)
    pass
