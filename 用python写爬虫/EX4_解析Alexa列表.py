# -*- coding: utf-8 -*-
"""从top-1m.csv中抽取域名数据, 一共百万个"""
import csv
from 用python写爬虫.复用函数集合 import link_crawler, MongoCache


class AlexaCallback:
    """从Alexa中提取网站url数据 因为网站改版 所以改为从文件中提取"""
    def __init__(self, max_urls=20):
        """提取1000个网站的数据 太多的话费时间"""
        self.max_urls = max_urls
        self.seed_url = 'http://111.231.65.159/'

    def __call__(self, url, html):
        if url == self.seed_url:
            urls = []
            for _, website in csv.reader(open('top-1m.csv')):
                urls.append('http://' + website)
                if len(urls) == self.max_urls:
                    break
            return urls

# A = AlexaCallback()
# A('test', '121')

if __name__ == '__main__':
    scrape_callback = AlexaCallback()
    link_crawler(seed_url='http://111.231.65.159/', cache=MongoCache(),
                 scrape_callback=scrape_callback)