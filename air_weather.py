# -*- coding: utf-8 -*-
"""
Project: MrYu-Github
Creator: Weather_Pm2.5
Create time: 2019-10-28 10:58
Introduction: 获取空气质量
官网：https://www.juhe.cn
{"reason": "查询成功", "result": { "city": "深圳",
"realtime": {
"temperature": "26", "humidity": "80", "info": "阴", "wid": "02", "direct": "西北风", "power": "3级", "aqi": "80" },
 "future": [ { "date": "2019-10-28", "temperature": "1/7℃", "weather": "小雨转多云", "wid": { "day": "07", "night": "01" }, "direct": "北风转西北风" }, "error_code": 0 }
"""
import requests
import datetime

Proxy = {
    "http": "http://127.0.0.1:12639",
    "https": "https://127.0.0.1:12639",
}

# 获取当前时间
today = datetime.datetime.now()
hour_time = today.strftime('%Y')
min_time = today.strftime('-%m-%d').replace("0", "")
now_time = hour_time + min_time

#处理提取天气情况
def air_weather(city):
    """
    通过城市名获取空气质量
    官网：https://www.juhe.cn
    token 申请地址：https://www.juhe.cn/docs/api/id/73
    :param city: 城市
    :return:
    """
    WeathToKey = '03f719480ada28fcc0857a946eeffa49' # Token
    AIR_STATUS_DICT = {
        50: '优',
        100: '良',
        150: '轻度污染',
        200: '中度污染',
        300: '重度污染',
        3000: '严重污染'
    }
    thunder_info = ["大雨转雷阵雨", "大雨转阵雨", "小雨", "雷阵雨", "雪","暴雨","雷阵雨"]
    overcast_info = ["晴转多云", "多云", "阴", "阴转多云", "阴转小雨", "阴转雷阵雨", "阴转雨"]
    if not city or not city.strip():
        return
    print('获取 {} 的空气质量...'.format(city))
    try:
        url = 'http://apis.juhe.cn/simpleWeather/query?city={city}&key={WeathToKey}'.format(city=city, WeathToKey=WeathToKey)
        resp = requests.get(url=url,proxies=Proxy)
        if resp.status_code == 200:
            print(resp.text)
            content_dict = resp.json()
            if content_dict.get('reason') == '查询成功!':
                nowTime = datetime.datetime.now().strftime('%Y-%m-%d')  # 获取本地计算机当前时间
                data_dict = content_dict['result']
                print(data_dict)
                date=data_dict['future'][0]['date']                 #时间
                temperature=data_dict['future'][0]['temperature']   #温度，最低温/最高温
                weather=data_dict['future'][0]['weather']           #天气情况
                now_direct = data_dict['future'][0]['direct']
                aqi=int(data_dict['realtime']['aqi'])#空气质量指数，可能为空
                direct = data_dict['realtime']['direct']
                power = data_dict['realtime']['power']
                air_status = '严重污染'
                if nowTime ==date:
                    for key in sorted(AIR_STATUS_DICT):
                        if key >=aqi:
                            air_status = AIR_STATUS_DICT[key]
                            break
                    weathers = '{city},今日气温：{temperature} {weather}\n'.format(city=city,weather=weather,temperature=temperature)
                    power = '大部分地区{now_direct}，少量地区{direct}{power}\n'.format(now_direct=now_direct, direct=direct,power=power)
                    pm = "空气PM2.5质量：{air_status}\n".format(aqi=aqi, air_status=air_status)
                    matter = "温馨提示：今日气候不佳亲记得早上出门带伞关好窗门哦！\n"
                    yu = "温馨提示：阴雨天气也不要掉以轻心适当做好防虫防雨工作哦！\n"
                    sum = "警告：未配置对应字典，请先系统录入避免Tips与天气不一致！\n"
                    update = "最新同步时间：{} Jenkins自动推送".format(today)
                    if weather in thunder_info:
                        weather_info = (weathers + power + pm + matter + update)
                    elif weather in overcast_info:
                        weather_info = (weathers + power + pm + yu + update)
                    else:
                        weather_info = (weathers + power + pm + sum + update)
                return weather_info
            else:
                print('获取空气质量失败:{}'.format(content_dict['data']))
                return None
    except Exception as exception:
        print(str(exception))
        return None



#机器人模拟发送
def postrsg(weather_info):
    data = {
        "msgtype": "text",
        "text": {
            "content": weather_info
        }
    }
    print(data)
    rsq = requests.post(url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b3b0cc66-87d3-4cab-9a15-541a477b3ff5',json=data, proxies=Proxy)
    print(rsq.text)

if __name__ == '__main__':
    city = '深圳'
    sendmsg = air_weather(city)
    print(sendmsg) #企业微信机器人
    # postrsg(request)
