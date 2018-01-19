# -*- coding: utf-8 -*-
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

session = requests.Session()

req = requests.get("http://example.webscraping.com/places/default/user/login")
cookies = req.cookies
html = req.text
params = parse_html(html)
params['email'] = 'test@123.com'
params['password'] = 'test'

response = session.post("http://example.webscraping.com/places/default/user"
                        "/login", params, cookies=cookies)
login_cookies = response.cookies

edit_request = requests.get(
    'http://example.webscraping.com/places/default/edit/Afghanistan-1',
    cookies=login_cookies)
params = parse_html(edit_request.text)
print(params)
params['population'] = str(int(params['population']) + 1)
post = session.post(
    'http://example.webscraping.com/places/default/edit/Afghanistan-1', params,
    cookies=edit_request.cookies)
print(post.status_code)
print(post.url)
