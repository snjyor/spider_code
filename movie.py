import urllib.request
import re
from lxml import etree
import pandas as pd
from scrapy.selector import Selector
import time

pd.set_option('display.max_columns', 20)

def open_url(url):
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    global result
    try:
        request = urllib.request.Request(url, headers=header)
        res = urllib.request.urlopen(request)
        result = res.read().decode('utf-8')
    except Exception as err:
        print(err)
    # print(result)
    return result

def scrapy_extrct(result):
    selector = Selector(text=result)
    result = selector.xpath('/html/body/div/h3').extract()
    print(result)

def hot_new_extrct(result):
    selector = etree.HTML(result)
    hot_and_new = selector.xpath('//*[@class="tit"]/a/text()')
    # print('hot_and_new:',hot_and_new)

    hot_and_new_links = selector.xpath('//*[@class="img"]/a/img/@src')
    # for link in hot_and_new_links:
    #     print(link)

    query_params = selector.xpath('//*[@class="tit"]/a/@href')
    # for query in query_params:
    #     print('query:',query)

    dict = {'name': [], 'year': [],'link':[],'img_link':[]}
    front_fix = 'http://www.rarbt.cc'
    for movie in hot_and_new:
        name = movie.split('/')[0]
        year = movie.split('.')[-1]
        dict['name'].append(name)
        dict['year'].append(year)
    for query in query_params:
        dict['link'].append(front_fix+query)
    for link in hot_and_new_links:
        dict['img_link'].append(link)
    df = pd.DataFrame(dict)
    print(df)
    df.to_csv('hot_and_new_movie.csv',encoding="utf-8", mode="a", header=True, index=True)

def newest_movies(result):
    selector = etree.HTML(result)

    movie_names = selector.xpath('//*[@class="tt cl"]/a/@title')
    pub_times = selector.xpath('//*[@class="tt cl"]/span/font/text()')
    links = selector.xpath('//*[@class="tt cl"]/a/@href')
    front_fix = 'http://www.rarbt.cc'

    # print(movie_names)
    # print(pub_times)
    # print(links)

    dict = {'name':[],'pub_date':[],'link':[]}
    for name in movie_names:
        dict['name'].append(name)
    for time in pub_times:
        dict['pub_date'].append(time)
    for link in links:
        url = front_fix + link
        dict['link'].append(url)
    df = pd.DataFrame(dict)
    return df

if __name__ == '__main__':
    for i in range(1,948):
        url = 'http://www.rarbt.cc/index.php/index/index/p/' + str(i) + '.html'
        result = open_url(url)
        # hot_new_extrct(result)
        df = newest_movies(result)
        # df.to_csv('./{0}.csv'.format(i), encoding='utf-8',mode="a", header=True, index=True)
        print(i)
        print(df)
        # exit('exit')

