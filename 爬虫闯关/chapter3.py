# -*- coding: utf-8 -*-
"""url: http://www.heibanke.com/lesson/crawler_ex02/"""
import requests
from bs4 import BeautifulSoup

from 爬虫闯关.chapter2 import parse_html, pass_chapter2

USERNAME = '123312'
PASSWORD = '123123'
login_url = 'http://www.heibanke.com/accounts/login'
seed_url = "http://www.heibanke.com/lesson/crawler_ex02/"


def login():
    """登陆后返回session"""
    global USERNAME, PASSWORD
    session = requests.Session()
    website = session.get(login_url)
    html = website.text
    params = parse_html(html)
    params['username'] = USERNAME
    params['password'] = PASSWORD
    session.post(login_url, params)
    return session


def pass_c3():
    session = login()
    token = session.get(seed_url).cookies['csrftoken']
    params = {}
    params['username'] = USERNAME
    params['csrfmiddlewaretoken'] = token
    for i in range(1, 31):
        params['password'] = i
        html = session.post(seed_url, params).text
        soup = BeautifulSoup(html, 'lxml')
        if soup.find('h3').text != "您输入的密码错误, 请重新输入":
            return params['password']

if __name__ == '__main__':
    print(pass_c3())