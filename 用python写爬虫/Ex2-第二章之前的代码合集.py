# -*- coding: utf-8 -*-
"""
可复用的函数集合
参考地址：https://bitbucket.org/wswp/code/src/tip/chapter01/link_crawler3.py
"""
import os
import re
import requests
import time
import csv
from queue import deque
from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.robotparser import RobotFileParser
from datetime import datetime

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/63.0.3239.132 Safari/537.36"


def link_crawler(seed_url, link_regex, user_agent='wswp', delay=5,
                 max_depth=-1, max_urls=-1, scrape_callback=None):
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
    # 仍然需要爬行的URL的队列
    crawl_queue = deque([seed_url])
    # URL深度
    seen = {seed_url: 0}
    # 跟踪已经下载了多少url
    num_urls = 0
    # 读取robots.txt内容
    rp = get_robots(seed_url)
    # 设置等待时间
    throttle = Throttle(delay)
    # headers = headers or {}
    while crawl_queue:
        url = crawl_queue.pop()
        # 检验该url在robots.txt是否禁止爬虫访问
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download_url(url, user_agent)
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
                    print(link)
                    link = normalize(seed_url, link)
                    # 检查链接是否已经抓取过
                    if link not in seen:
                        seen[seed_url] = depth + 1
                        # 检查链接是否处于同一深度
                        if same_domain(seed_url, link):
                            # 添加新链接在队列中
                            crawl_queue.append(link)
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print("robots.txt禁止访问此url：", url)
    print("下载完成, 下载url数量:", str(num_urls))


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


def download_url(url, user_agent='wswp', num_retries=2):
    """
    下载函数 传入url 可捕获异常，重试下载并设置用户代理
    num_retries 是重试次数 默认为2
    """
    print("下载中：", url)
    session = requests.Session()
    headers = {'User-agent': user_agent,
               "Accept": "text/html,application/xhtml+xml,application/xml;"
                         "q=0.9,image/webp,image/apng,*/*;q=0.8"
               }
    # 代理
    proxies = {
        # "http": "http://" + ip,
        # "https": "https://" + ip
    }
    try:
        html = session.get(url, headers=headers, proxies=proxies).text
    except URLError as e:
        print("捕获异常：", e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # 重试 5XX Http error
                return download_url(url, user_agent, num_retries-1)
    return html


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
    rp.read()
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
                 user_agent=user_agent, max_depth=2, delay=1,
                 max_urls=-1, scrape_callback=ScrapeCallback())
