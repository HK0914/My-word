import requests
from requests.exceptions import RequestException
import re
import json
import time
# from multiprocessing import Pool pool = Pool()  pool.map(main,[i*10 for i in range(10)])

def get_one_page(url):
    try:
        headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException :
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield{
            '名次': item[0],
            '图片链接': item[1],
            '影名': item[2],
            '主演': item[3].strip()[3:],
            '上映时间' : item[4].strip()[5:],
            '得分': item[5]+item[6]
        }

def write_to_file(content):
    with open('猫眼电影Top100爬虫.txt','a', encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii = False)+'\n')

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html =get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ =='__main__':
    for i in range(10):
        main(offset = i * 10)
        time.sleep(1)
