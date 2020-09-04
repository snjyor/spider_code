import urllib.request
from lxml import etree
import time
import pandas as pd
import os

def open_url(url):
    # print(url)
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    global result

    try:
        request = urllib.request.Request(url, headers=header)
        res = urllib.request.urlopen(request, timeout=5)
        result = res.read().decode('utf-8')
    except Exception as err:
        print(err)
    return result


def data_extract(query_params):
    front_fix = 'https://www.tianqi.com'
    dict = {"city": [], "date": [], "week": [], "lunar": [], "temperature": [], "state": [], "lowest_temp": [],
            "highest_temp": [], "humidity": [], "wind": [], "wind_level": [], "ultraviolet": [], "air_quality": [],
            "pm_value": [], "sunrise": [], "sunset": []}
    count = 1
    for query_param in query_params:
        url = front_fix + query_param
        local_result = open_url(url)
        selector = etree.HTML(local_result)
        try:
            city = selector.xpath('//*[@class="name"]/h2/text()')[0]
            week = selector.xpath('//*[@class="week"]/text()')[0]
            temperature = selector.xpath('//*[@class="now"]/b/text()')[0]
            # dushu = selector.xpath('//*[@class="now"]/i/text()')[0]
            state = selector.xpath('//*[@class="weather"]/span/b/text()')[0]
            temperature_arange = selector.xpath('//*[@class="weather"]/span/text()')[0]
            humidity = selector.xpath('//*[@class="shidu"]/b/text()')
            air_quality = selector.xpath('//*[@class="kongqi"]/h5/text()')[0]
            pm_value = selector.xpath('//*[@class="kongqi"]/h6/text()')[0]
            sun = selector.xpath('//*[@class="kongqi"]/span/text()')
        except Exception as err:
            print(err)
        else:

            date = week.strip().split()
            temperature_arange = temperature_arange.strip('℃').split(' ~ ')

            try:
                dict['city'].append(city)
                dict['date'].append(date[0])
                dict['week'].append(date[1])
                dict['lunar'].append(date[2])
                dict['temperature'].append(temperature)
                dict['state'].append(state)
                dict['lowest_temp'].append(temperature_arange[0])
                dict['highest_temp'].append(temperature_arange[1])
                dict['humidity'].append(humidity[0].split("：")[1])
                dict['wind'].append(humidity[1].split("：")[1].split(" ")[0])
                dict['wind_level'].append(humidity[1].split("：")[1].split(" ")[1])
                dict['ultraviolet'].append(humidity[2].split("：")[1])
                dict['air_quality'].append(air_quality.split("：")[1])
                dict['pm_value'].append(pm_value.split(": ")[1])
                dict['sunrise'].append(sun[0].split(": ")[1])
                dict['sunset'].append(sun[1].split(": ")[1])
            except Exception as err:
                print(err)
            else:
                df = pd.DataFrame(dict)

                if len(df)==50: # 保存文件并清空字典
                    df.to_csv('./spider/'+str(count)+'.csv', encoding="utf-8", mode="a", header=True, index=True)
                    dict = {"city": [], "date": [], "week": [], "lunar": [], "temperature": [], "state": [],
                            "lowest_temp": [],"highest_temp": [], "humidity": [], "wind": [], "wind_level": [],
                            "ultraviolet": [],"air_quality": [],"pm_value": [], "sunrise": [], "sunset": []}
                    print(count)
                    count += 1


            # print(city)
            # print(date)
            # print(temperature)
            # print(state)
            # print('weather:', temperature_arange)
            # print(humidity)
            # for i in humidity:
            #     i = i.split('：')
            #     print(i)
            # print(air_quality)
            # print(pm_value)
            # print(sun)


            # with open('china_weather.txt', 'a') as f:
            #     f.write('*' * 100 + os.linesep)
            #     f.write(url + os.linesep)
            #     f.write(city + os.linesep)
            #     f.write(week + os.linesep)
            #     f.write(temperature + dushu + os.linesep)
            #     f.write(state + os.linesep)
            #     f.write(temperature_arange + os.linesep)
            #     for i in shidu:
            #         f.write(i + os.linesep)
            #     f.write(kongqi + os.linesep)
            #     f.write(pm_value + os.linesep)
            #     for j in sun:
            #         f.write(j + os.linesep)
            #     f.close()


def local_city(result):
    selector = etree.HTML(result)

    hotcities = selector.xpath('//*[@class="hotcity"]/span/a/text()')
    hotcity_querys = selector.xpath('//*[@class="hotcity"]/span/a/@href')

    provinces = selector.xpath('//*[@class="citybox"]/h2/a/text()')
    province_querys = selector.xpath('//*[@class="citybox"]/h2/a/@href')

    cities = selector.xpath('//*[@class="citybox"]/span/h3/a/text()')
    city_qureys = selector.xpath('//*[@class="citybox"]/span/h3/a/@href')

    towns = selector.xpath('//*[@class="citybox"]/span/a/text()')
    town_querys = selector.xpath('//*[@class="citybox"]/span/a/@href')

    query_params = hotcity_querys + province_querys + city_qureys + town_querys

    # print(provinces)
    # print(province_querys)
    #
    # print(cities)
    # print(city_qureys)
    #
    # print(towns)
    # print(town_querys)

    return query_params


if __name__ == '__main__':
    print("开始执行……")
    start = time.time()

    url = 'https://www.tianqi.com/chinacity.html'
    result = open_url(url)
    query_params = local_city(result)
    data_extract(query_params)

    end = time.time()
    print("运行结束……")
    expense = end - start
    print("全国天气数据获取耗时：", expense)
