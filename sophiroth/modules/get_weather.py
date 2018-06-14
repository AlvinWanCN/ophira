#coding:utf-8
import urllib2
from lxml import etree
import re
host = 'http://tianqi.2345.com'
path = '/today-58362.htm'
url = host + path
content = urllib2.urlopen(url).read()
html = etree.HTML(content)

def get_status():  ##获取天气状况
    try:
        weather_status = html.xpath('//*[@id="wrap"]/div[4]/div[1]/div[3]/dl[1]/dd/ul/li[1]/span[2]')[0].text
        if weather_status:
            return weather_status
    except Exception as e:
        print(e)
        return "unknow"

def get_max_temperature():  # 获取最高气温
    # weather_max_temperature=re.findall(r'</b>(-?\d)<i>',str(content))[0]
    try:
        weather_max_temperature = html.xpath('//*[@id="wrap"]/div[4]/div[1]/div[3]/dl[1]/dd/ul/li[2]/span/text()')[
            0]
        if weather_max_temperature:
            return weather_max_temperature
    except Exception as e:
        print(e)
        return "unknow"

def get_min_temperature():  # 获取最低气温
    try:
        weather_min__temperature = re.findall(r'</b>(-?\d+)<i>', str(content))[-1]
        if weather_min__temperature:
            return weather_min__temperature
    except Exception as e:
        print(e)
        return "unknow"



if __name__ == '__main__':
    print(get_max_temperature())