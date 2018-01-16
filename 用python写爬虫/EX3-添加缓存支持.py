# -*- coding: utf-8 -*-
"""重构DownLoader函数 添加缓存功能"""
import re
import requests
import time
import random
from queue import deque
from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.robotparser import RobotFileParser
from datetime import datetime

# 默认用户代理
DEFAULT_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                "AppleWebKit/537.36 (KHTML, like Gecko) " \
                "Chrome/63.0.3239.132 Safari/537.36"
# 默认等待延迟
DEFAULT_DELAY = 5
# 默认重连次数
DEFAULT_RETRIES = 1
# 默认等待超时
DEFAULT_TIMEOUT = 60


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


class DownLoader:
    """下载网页源码"""
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT,
                 timeout=DEFAULT_TIMEOUT, proxies=None,
                 num_retries=DEFAULT_RETRIES, cache=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies or {}
        self.num_retries = num_retries
        self.cache = cache
        self.timeout = timeout

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url 没有在缓存中
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # 服务器错误，因此忽略缓存和重新下载的结果
                    result = None
        if result is None:
            # 结果没有从缓存加载，还需下载
            self.throttle.wait(url)
            headers = {'User-agent': self.user_agent,
                       "Accept": "text/html,application/xhtml+xml,"
                                 "application/xml;q=0.9,image/webp,"
                                 "image/apng,*/*;q=0.8"
                       }
            result = self.download(url, headers, num_retries=self.num_retries)
            if self.cache:
                # 存储结果到缓存中
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, num_retries, data=None):
        """下载函数 返回一个字典 两个关键字分别是html 和 code"""
        print("下载中: ", url)
        session = requests.Session()
        try:
            req = session.get(url, headers=headers, proxies=self.proxies,
                              timeout=self.timeout)
            html = req.text
            code = req.status_code
        except Exception as e:
            print("下载中出现错误", str(e))
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    return self.download(url, headers, num_retries-1, data)
            else:
                code = None
        return {'html': html, 'code': code}

