# -*- coding: utf-8 -*-
"""更改ip用函数"""
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
import socket
import socks
import requests
import re
import functools


def new_identity():
    """获取一个新的tor的ip"""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


def use_proxy(func):
    """该装饰器作用：使用tor代理"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
            socket.socket = socks.socksocket
        except Exception as e:
            print("可能未打开tor浏览器?")
            print("错误信息: {}".format(e))
        return func(*args, **kwargs)
    return wrapper


def get_proxy_by_181():
    """获取 http://www.ip181.com/ 更新的100个代理ip
        还有一个 http://www.xicidaili.com/nn/
    """
    ips = []
    ports = []
    res = requests.get("http://www.ip181.com/").text
    soup = BeautifulSoup(res, 'lxml')
    tds = soup.find_all('td')
    for td in tds:
        if re.match('^([0-9]|\.)+$', td.text):
            if len(td.text) > 6:
                ips.append(td.text)
            else:
                ports.append(td.text)
    L = list(map(lambda x, y: ":".join([x, y]), ips, ports))
    with open('ip.txt', 'w') as f:
        for ip in L[:20]:
            f.write(ip + "\n")


@use_proxy
def get_proxies_by_cn():
    """获取http://cn-proxy.com/ 中前十个代理ip
       需要使用tor
    """
    session = requests.Session()
    res = session.get('http://cn-proxy.com/')
    trs = 'hh'
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        tables = soup.find_all(class_='table-container')
        if tables:
            table = tables[-1]
            trs = table.find('tbody').find_all('tr')

    if trs:
        with open('ip.txt', 'a+') as f:
            for tr in trs[:10]:
                f.write(tr.contents[1].text + ":" + tr.contents[3].text + "\n")


def get_ips():
    get_proxy_by_181()
    get_proxies_by_cn()
    ips = []
    with open('ip.txt', 'r') as f:
        for i in f:
            ips.append(i.strip())
    return ips

