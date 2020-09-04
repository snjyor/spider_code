import urllib.request
from lxml import etree

def open_url(url):
    header ={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    global result
    try:
        response = urllib.request.Request(url,headers=header)
        res = urllib.request.urlopen(response,timeout=5)
        result = res.read().decode('utf-8')
    except Exception as err:
        print(err)

    return result

def extract_text(result):
    selector = etree.HTML(result)
    # texts = selector.xpath('//*[@class="content"]/span/text()')
    inner_links = selector.xpath('//*[@class="article block untagged mb15 typs_hot"]/a/@href')
    front_fix = 'https://www.qiushibaike.com'
    # for text in texts:
    #     print(text)
    inner_links = list(set(inner_links))
    for link in inner_links:
        url = front_fix + link
        print(url)
        result = open_url(url)
        inner_content(result)

def inner_content(result):
    selector = etree.HTML(result)
    texts = selector.xpath('//*[@class="content"]/text()')
    print(texts)
    with open('./qiushibaike.txt','a') as f:
        for text in texts:
            f.write(text)
        f.write('\n')
        f.write('\n')
        f.close()

if __name__ == '__main__':
    for i in range(1,14):
        url = 'https://www.qiushibaike.com/text/page/'+str(i)+'/'
        result = open_url(url)
        extract_text(result)


