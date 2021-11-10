import json

import requests
from lxml import etree
from copyheaders import headers_raw_to_dict
import os

pic_path = "/Users/apple/Pictures/desktop_pic/"


def request():
    header_raw = b'''
            Accept: application/json, text/javascript, */*; q=0.01
            Accept-Encoding: gzip, deflate, br
            Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
            Cache-Control: no-cache
            Connection: keep-alive
            DNT: 1
            Host: bird.ioliu.cn
            Origin: https://ss.netnr.com
            Pragma: no-cache
            Referer: https://ss.netnr.com/
            Sec-Fetch-Dest: empty
            Sec-Fetch-Mode: cors
            Sec-Fetch-Site: cross-site
            User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36
        '''
    header = headers_raw_to_dict(header_raw)
    pic_type_dict = {
        36:"4k专区",
        6:"美女模特",
        9:"风景大片",
        15:"小清新",
        26:"动漫卡通",
        14:"萌宠动物",
        10:"炫酷时尚",
        29:"月历壁纸"
    }
    for key, value in pic_type_dict.items():
        urls = []
        for i in range(1, 1000, 100):
            url = "https://bird.ioliu.cn/v2?url=http%3A%2F%2Fwallpaper.apc.360.cn%2Findex.php%3Fc%3DWallPaper%26start%3D" + \
                  str(i) + "%26count%3D" + str(i+99) + "%26from%3D360chrome%26a%3DgetAppsByCategory%26cid%3D"+str(key)
            response = requests.get(url, headers=header)
            html_dict = json.loads(response.text)
            for data in html_dict.get('data'):
                urls.append(data.get('url'))
        print(len(urls))
        save_pic(urls, value)
        print(key, value)


def save_pic(urls, value):
    for url in urls:
        print(url)
        response = requests.get(url)
        if not os.path.exists(pic_path+value+"/"):
            os.mkdir(pic_path+value+"/")
        with open(pic_path+value+"/"+url.split('/')[-1], "wb") as file:
            file.write(response.content)


if __name__ == '__main__':
    request()
