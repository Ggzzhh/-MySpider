# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urldefrag, urljoin

session = requests.Session()
base_url = "http://www.heibanke.com/lesson/crawler_ex00/"


def return_pwd(url):
    """返回通关密码"""
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('h3').text
    return res


def normalize(seed_url, link):
    """通过删除hash值和添加域来规范化链接"""
    link, _ = urldefrag(link)
    return urljoin(seed_url, link)


if __name__ == "__main__":
    pwd = return_pwd(base_url)[-5:]
    while True:
        link = normalize(base_url, pwd)
        print(link)
        res = return_pwd(link)
        print(res)
        pwd = re.search('[0-9]+', res).group()

