# -*- coding: utf-8 -*-
"""
第二关  其实改改url 就能过关...... 不过既然。。。就。。。
"""
import requests
from bs4 import BeautifulSoup


def parse_html(html):
    """
    解析html文件并返回一个表单字典
    :param html: 获取的html
    :return: {}
    """
    data = {}
    soup = BeautifulSoup(html, 'lxml')
    for e in soup.findAll('input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def pass_chapter2(url, data, cookies=None):
    session = requests.Session()
    res = session.post(url, data, cookies)
    print(res)
    soup = BeautifulSoup(res.text, 'lxml')
    if soup.find('h3').text != "您输入的密码错误, 请重新输入":
        return data['password']

if __name__ == "__main__":
    res = requests.get("http://www.heibanke.com/lesson/crawler_ex01/")
    html = res.text
    # cookies = res.cookiess
    data = parse_html(html)
    data['username'] = 'test'
    url = "http://www.heibanke.com/lesson/crawler_ex01/"
    for i in range(1, 31):
        data['password'] = i
        print(pass_chapter2(url, data))
