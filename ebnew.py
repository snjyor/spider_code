import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery
from lxml import etree
import csv
import pandas as pd


def post_html(url, searchword, pagenum, type):
    header = {
        'Cookie': '__cfduid = d251f6ce9d8d13d5ba28f5d7c2003542c1599110219;JSESSIONID = 9939F3669785EB24C0AAC84E2E258A80;userType = 12;loginUser=',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }

    data = {'key': searchword, 'currentPage': pagenum, 'infoClassCodes': type}
    res = requests.post(url, headers=header, data=data)
    html = res.text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()

    return html


def get_html(url):
    header = {
        'Cookie': '__cfduid=d251f6ce9d8d13d5ba28f5d7c2003542c1599110219; userType=12; loginUser=; JSESSIONID=1BF688D7E68456EFFFBDB551FC92995C',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'lxml')
    html = soup.prettify()

    return html


def extract_link(html):
    selector = etree.HTML(html)
    links = selector.xpath('//*[@class="fl line-h26 abstract-title font-16 width-75 line-h20"]/@href')
    titles = selector.xpath('//*[@class="ebnew-content-list"]//div/div/a/@title')
    return links, titles


def extract_inner_data(html):
    selector = etree.HTML(html)
    # 采购时间，采购人名称，采购价格，还有采购设备信息
    text_list = selector.xpath('//*[@class="detials-content mg-t20 font-14 color-666 pd-b15"]/text()')
    message_list = []
    # print(text_list)
    for i in text_list:
        try:
            message_list.append(i.strip().split('：')[1])
        except Exception as err:
            # print(err)
            message_list.append('null')
    return message_list


def save_csv(message_list):
    with open('ebnew.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [message_list[0], message_list[1], message_list[2], message_list[3], message_list[4], message_list[5],
             message_list[6], message_list[7], message_list[8], message_list[9], message_list[10]])


if __name__ == '__main__':
    url = 'https://ss.ebnew.com/tradingSearch/index.htm'
    print(url)
    searchword = '直线加速器'
    type = 'zbjggg'
    link_list = []
    title_list = []
    for pagenum in range(1, 101):
        html = post_html(url, searchword, pagenum, type)
        links, titles = extract_link(html)
        link_list += links
        title_list += titles
    # print(link_list)
    # print(title_list)
    fieldnames = ['项目名称', '项目编号', '招标范围', '招标机构', '招标人', '开标时间', '公示时间', '中标结果公告时间', '中标人', '制造商', '制造商国家或地区']
    save_csv(fieldnames)
    for i in range(0, len(title_list)):
        if '中标结果公告' in title_list[i]:
            html = get_html(link_list[i])
            message_list = extract_inner_data(html)
            # print(message_list)
            print(link_list[i])
            if len(message_list) == 12:
                save_csv(message_list)
