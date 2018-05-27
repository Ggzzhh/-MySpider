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

    def __init__(self, proxy=None, delay=DELAY, num_retries=NUM_RETRIES,
                 timeout=TIMEOUT, headers=HEADERS, encoding=ENCODING,**kwargs):
        """
        初始化
        :param proxy: 下载时使用的代理
        :param delay:  下载延迟
        :param timeout: 下载超时时间
        :param headers: 下载时使用的文件头
        :param num_retries: 下载重试次数
        :param kwargs:  其他
        """
        self.proxy = proxy
        self.timeout = timeout
        self.headers = headers or {'User-agent': 'OSpider'}
        self.logging = logger
        self.throttle = Throttle(delay)
        self.num_retries = num_retries
        self.encoding = encoding
        self.kwargs = kwargs

    def __call__(self, url, method='GET', data=None, cookies=None, **kwargs):
        """
        这个魔法函数可以让类的实例像函数一样被调用，例如：
        D = DOWNLOAD(...)
        result = D(url)
        :param url:  url
        :param method:  请求的方法
        :param data:    请求的内容
        :param cookies: 请求时使用的cookies
        :param kwargs:  其他，比如代理
        :return: {'html': 网页内容, 'status': 状态码, 'url': 请求地址}
        """
        # 设置同个域下的限速
        self.throttle.wait(url)
        # 让类的实例返回download函数的返回值
        return self.download(url, method, data, cookies)

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
        # 设置头信息
        session.headers = self.headers
        # 设置代理
        if self.proxy:
            if isinstance(self.proxy, dict):
                if self.proxy.get('http') or self.proxy.get('https'):
                    session.proxies = self.proxy
                    self.logging.info('设置代理:{}'.format(self.proxy))
            else:
                self.logging.error('代理格式错误，需要使用字典格式')
        # 检查请求方法
        if method not in methods:
            raise ValueError("请求方法错误, 请在{}中选择!".format(methods))
        # 设置cookies
        if cookies:
            session.cookies = cookies
        # 获取内容并返回
        try:
            res = session.request(method, url, data=data)
            res.encoding = self.encoding or 'utf-8'
            html = res.text
            status = res.status_code
        # 出现问题打印到日志，然后重试num_retries次
        except Exception as e:
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if self.num_retries > 0 and 500 <= code < 600:
                    self.num_retries -= 1
                    return self.download(url, method, data, cookies)
            else:
                code = None
            self.logging.error(e)
            html = None
            status = None
        return {'html': html, 'status': status, 'url': url}