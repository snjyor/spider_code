import requests
import json
import time
from lxml import etree
import pandas as pd
from copyheaders import headers_raw_to_dict
pd.set_option("display.max_columns", None)


def get_proxy():
    return requests.get("http://localhost:5010/get/").json()


def requester(url):
    sess = requests.session()
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}

    whole_data = []
    whole_hrefs = []
    for num in range(1, 501, 25):
        full_url = url + str(num)
        hrefs = mult_request(sess, full_url, headers=headers)
        whole_hrefs.extend(hrefs)
    print(whole_hrefs)
    print(f"len of whole: {len(whole_hrefs)}")
    for href in whole_hrefs:
        try:
            one = inner_requester(sess, href)
            whole_data.append(one)
        except Exception as err:
            print(f"inner request went wrong, detail:{err}")
            continue
    return whole_data


def mult_request(sess, full_url, headers):
    flag = True
    count = 0
    while flag:
        count += 1
        # proxy = get_proxy().get("proxy")
        # print(f"proxy:{proxy}")
        res = sess.get(full_url,
                       headers=headers,
                    #    proxies={"http": "http://{}".format(proxy)},
                       )
        selector = etree.HTML(res.text)
        # print(res.text)
        hrefs = selector.xpath("//*[@class='superlative-list__name font-light-bold']/@href")
        hrefs = ["https://www.wine-searcher.com" + href for href in hrefs]
        if len(hrefs) != 0:
            break
        print("waitting...")
        time.sleep(60)
        if count >= 5:
            break
    return hrefs


def inner_mult_request(sess, url, headers):
    flag = True
    count = 0
    while flag:
        count += 1
        proxy = get_proxy().get("proxy")
        print(f"inner requester proxy:{proxy}")
        detail_res = sess.get(url,
                              headers=headers,
                              proxies={"http": "http://{}".format(proxy)},
                              )
        selector = etree.HTML(detail_res.text)
        wine_name = selector.xpath(
            "//*[@class='product-details__container-right d-flex flex-column mt-4A mt-md-0 pl-0 mb-0']/li[1]/h1/text()")
        if len(wine_name) != 0:
            break
        if count >= 5:
            break
        print(f"inner waitting...")
        time.sleep(60)
    return selector, wine_name

def inner_requester(sess, url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}

    detail_url = url + "#t2"
    print(f"inner url:{detail_url}")
    selector, wine_name = inner_mult_request(sess, detail_url, headers)
    price = selector.xpath("//*[@class='d-inline-block pl-2A pl-md-0']/ul/li/strong[@class='text-nowrap']/text()")[0]
    region = selector.xpath("//*[@class='row']/div[2]/div[3]/a/text()")
    wine_name = beautistr(wine_name[0])
    price = beautistr(price)
    data = {
        "wine_name": wine_name,
        "price": price,
        "region": region[::-1]
    }
    return data

def beautistr(string):
    result = string.replace("  ", "").replace("\n", "").replace(",", "")
    return result


def parser(content):
    df = pd.DataFrame(content)
    regions = []
    for regi in data:
        regions.append(regi.get("region"))
    df2 = pd.DataFrame(regions)
    df3 = pd.concat((df, df2), axis=1)
    print(df3)

    df3.to_excel("wine_burgundy.xlsx")

if __name__ == '__main__':
    url = "https://www.wine-searcher.com/regions-burgundy/"
    content = requester(url)
    parser(content)
