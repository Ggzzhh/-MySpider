# -*- coding: utf-8 -*-
"""
可复用的函数集合
参考地址：https://bitbucket.org/wswp/code/src/tip/chapter01/link_crawler3.py
"""
import os
# 保持打开状态
import pickle
# 压缩以及解压
import zlib
import re
import requests
import time
import csv
import hashlib
from queue import deque
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag, urlsplit
from urllib.robotparser import RobotFileParser
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.binary import Binary

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


def link_crawler(seed_url, link_regex=None, user_agent='wswp', delay=5,
                 proxies=None,
                 max_depth=-1, max_urls=-1, scrape_callback=None, cache=None):
    """
    从给定的种子URL的正则表达式匹配的抓取链接以下链接
    seed_url 基础地址 如:https://www.baidu.com
    link_regex 筛选链接的正则表达式
    user_agent 头部信息中用户浏览器信息
    delay  下载页面间隔时间
    max_depth 搜索页数
    max_urls 最多存储url数
    scrape_callback 回调函数 完成下载后调用
    """
    start_time = datetime.now()
    # 仍然需要爬行的URL的队列
    crawl_queue = deque([seed_url])
    # URL深度
    seen = {seed_url: 0}
    # 跟踪已经下载了多少url
    num_urls = 0
    # 读取robots.txt内容
    rp = get_robots(seed_url)
    # 设置等待时间
    D = DownLoader(delay=delay, user_agent=user_agent, proxies=proxies,
                   cache=cache)
    while crawl_queue:
        url = crawl_queue.pop()
        # 检验该url在robots.txt是否禁止爬虫访问
        if rp.can_fetch(user_agent, url) or rp is None:
            html = D(url)
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])
            depth = seen[seed_url]
            if depth != max_depth:
                # 可以继续下一步抓取
                if link_regex:
                    # 过滤地址
                    links.extend(link for link in get_links(html) if
                                 re.match(link_regex, link))
                for link in links:
                    # print(link)
                    link = normalize(seed_url, link)
                    # 检查链接是否已经抓取过
                    if link not in seen:
                        seen[seed_url] = depth + 1
                        # 检查链接是否处于同一深度
                        # if same_domain(seed_url, link):
                            # 添加新链接在队列中
                        crawl_queue.append(link)
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print("robots.txt禁止访问此url：", url)
    print("下载完成, 下载url数量:", str(num_urls))
    print("花费时间：" + str(datetime.now() - start_time))


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
                if self.num_retries > 0 and (result['code'] is None or 500 <= \
                        result['code'] < 600):
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


class DiskCache:
    """
    磁盘缓存 可以跨平台 为每个网页保存一个缓存副本 比较占用空间
    默认过期时间是30天
    因为设置了__setitem__以及__getitem__所以
    可以像调用数组那样调用 如 : disk[url]
    """
    def __init__(self, cache_dir='cache', expires=timedelta(days=30)):
        self.cache_dir = cache_dir
        self.expires = expires

    def url_to_path(self, url):
        """把url的hash.md5值保存为文件名"""
        my_hash = hashlib.md5(bytes('crawler', encoding='utf-8'))
        my_hash.update(bytes(url, encoding='utf-8'))
        filename = my_hash.hexdigest()
        return os.path.join(self.cache_dir, filename)

    def has_expired(self, timestamp):
        """返回这个时间戳是否已经过期"""
        return datetime.utcnow() > timestamp + self.expires

    def __getitem__(self, url):
        """为这个URL从磁盘加载数据"""
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                result, timestamp = pickle.loads(zlib.decompress(fp.read()))
                if self.has_expired(timestamp):
                    raise KeyError(url + '已经过期')
                return result
        else:
            # URl 不在缓存中
            raise KeyError(url + '不存在')

    def __setitem__(self, url, result):
        """存储url数据到本地磁盘"""
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        timestamp = datetime.utcnow()
        data = pickle.dumps((result, timestamp))
        with open(path, 'wb') as fp:
            fp.write(zlib.compress(data))


class MongoCache:
    def __init__(self, client=None, expires=timedelta(days=30)):
        # 如果没有设置服务器 就尝试链接到默认端口
        self.client = MongoClient('localhost', 27017) \
            if client is None else client
        # 创建一个相当于表的集合来存储缓存
        self.db = self.client.cache

    def __contains__(self, url):
        """
        当使用in，not in 对象的时候 调用
        (not in 是在in完成后再取反,实际上还是in操作)
        """
        try:
            self[url]
        except KeyError:
            return False
        else:
            return True

    def __setitem__(self, url, result):
        """存储url及其数据到数据库"""
        # Binary + zlib + pickle 压缩数据
        record = {'result': Binary(zlib.compress(pickle.dumps(result))),
                  'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)

    def __getitem__(self, url):
        """读取数据库中的url的值"""
        record = self.db.webpage.find_one({'_id': url})
        if record:
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + '不存在')

    def clear(self):
        """删除所有数据"""
        self.db.webpage.drop()


def get_links(html):
    """以数组的形式返回网页中的所有链接"""
    bs_obj = BeautifulSoup(html, 'lxml')
    links = []
    for link in bs_obj.find_all('a'):
        links.append(link.get('href'))
    return links


def get_robots(seed_url):
    rp = RobotFileParser()
    rp.set_url(urljoin(seed_url, '/robots.txt'))
    try:
        rp.read()
    except Exception as e:
        return None
    return rp


def normalize(seed_url, link):
    """通过删除hash值和添加域来规范化链接"""
    link, _ = urldefrag(link)
    return urljoin(seed_url, link)


def same_domain(url1, url2):
    """如果两个链接处于同一域，返回True"""
    return urlparse(url1).netloc == urlparse(url2).netloc


class ScrapeCallback:
    """针对示例网站的回调函数"""
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))
        self.fields = ('area', 'population', 'iso', 'country', 'capital',
                       'continent', 'tld', 'currency_code', 'currency_name',
                       'phone', 'postal_code_format', 'postal_code_regex',
                       'languages', 'neighbours')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view/', url):
            soup = BeautifulSoup(html, 'lxml')
            row = []
            for field in self.fields:
                row.append(soup.find('table')
                           .find('tr', id='places_{}__row'.format(field))
                           .find('td', class_='w2p_fw').text)
            self.writer.writerow(row)

if __name__ == "__main__":
    # url = "https://www.whatismybrowser.com/" \
    #       "developers/what-http-headers-is-my-browser-sending"
    url = 'http://example.webscraping.com'
    link_crawler(url, '/(places/default/index|places/default/view)',
                 user_agent=DEFAULT_AGENT, max_depth=2, delay=1,
                 max_urls=-1, scrape_callback=ScrapeCallback(),
                 cache=DiskCache())

