# -*- coding: utf-8 -*-
import time
from datetime import datetime
from urllib.parse import urlparse

import requests

from OSpider.settings import *
from OSpider import logger
"""
    DOWNLOAD类是下载器，用于下载或者向url发出请求。
"""

__author__ = 'Ggzzhh'


class Throttle:
    """下载限速： 在两次下载之间添加延迟"""
    def __init__(self, delay):
        # 延迟时间
        self.delay = delay
        # 上次下载的时间戳
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            # 计算睡眠时间
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        # 更新上次睡眠时间
        self.domains[domain] = datetime.now()


class DOWNLOAD:

    def __init__(self, proxy=None, delay=DELAY,
                 timeout=TIMEOUT, headers=HEADERS, **kwargs):
        """
        初始化
        :param proxy: 下载时使用的代理
        :param delay:  下载延迟
        :param timeout: 下载超时时间
        :param headers: 下载时使用的文件头
        :param kwargs:  其他
        """
        self.proxy = proxy
        self.timeout = timeout
        self.headers = headers or {'User-agent': 'OSpider'}
        self.logging = logger
        self.throttle = Throttle(delay)
        self.kwargs = kwargs

    def __call__(self, url, method='GET', data=None, cookies=None, **kwargs):
        self.throttle.wait(url)
        res = self.download(url, method, data, cookies)
        return res

    def download(self, url, method='GET', data=None, cookies=None):
        """
        具体下载用函数
        :param url: 请求地址
        :param method: 请求方法
        :param data: 请求附带的内容
        :return: {'html': 网页内容, 'status': 状态码, 'url': 请求地址}
        """
        methods = ["GET", "POST", "PUT", "DELETE"]
        session = requests.Session()
        session.headers = self.headers
        if self.proxy:
            if isinstance(self.proxy, dict):
                if self.proxy.get('http') or self.proxy.get('https'):
                    session.proxies = self.proxy
            else:
                self.logging.error('代理格式错误，需要使用字典格式')
        if method not in methods:
            raise ValueError("请求方法错误, 请在{}中选择!".format(methods))
        if cookies:
            session.cookies = cookies
        try:
            res = session.request(method, url, data=data)
            html = res.text
            status = res.status_code
        except Exception as e:
            self.logging.error(e)
            html = None
            status = None
        return {'html': html, 'status': status, 'url': url}

if __name__ == '__main__':
    D = DOWNLOAD()
    res = D('http://ip.chinaz.com/')
    print(res)