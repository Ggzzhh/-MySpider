# -*- coding: utf-8 -*-
"""
并行爬虫 多线程爬取网站
为了支持使用数据库存储ip池 进行修改
"""

import time
import threading
import multiprocessing
from urllib.parse import urldefrag, urljoin
from datetime import datetime

from 用python写爬虫.复用函数集合 import DownLoader, MongoCache
from 用python写爬虫.EX4_解析Alexa列表 import AlexaCallback
from 用python写爬虫.EX4_单独存储队列_MongoDB import MongoQueue

SLEEP_TIME = 1


def threaded_crawler(seed_url, link_regex=None, user_agent='wswp', delay=5,
                     proxies=None, max_depth=-1, max_urls=-1, num_retries=1,
                     scrape_callback=None, cache=None, max_threads=10,
                     timeout=60):
    """
    从给定的种子URL的正则表达式匹配的抓取链接以下链接
    seed_url 基础地址 如:https://www.baidu.com
    link_regex 筛选链接的正则表达式
    user_agent 头部信息中用户浏览器信息
    delay  下载页面间隔时间
    max_depth 搜索页数
    max_urls 最多存储url数
    scrape_callback 回调函数 完成下载后调用
    num_retries 重连次数
    cache  缓存方法
    max_threads  最大线程数
    """
    start_time = datetime.now()
    # 为了让进程不混乱 必须在函数内链接mongo的服务器
    if cache is None:
        cache = MongoCache()
        cache.clear()
    # 多线式原本内容
    # crawl_queue = [seed_url]
    # seen = set([seed_url])
    crawl_queue = MongoQueue()
    crawl_queue.clear()
    crawl_queue.push(seed_url)
    D = DownLoader(cache=cache, delay=delay, user_agent=user_agent,
                   proxies=proxies, num_retries=num_retries, timeout=timeout)

    def process_queue():
        """进程队列"""
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                # 抓取队列空了
                break
            else:
                html = D(url)
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print('回调函数有误: {}---{}'.format(url, e))
                    else:
                        for link in links:
                            link = normalize(seed_url, link)
                            crawl_queue.push(link)
                crawl_queue.complete(url)
    # 等待所有下载线程完成
    threads = []
    while threads or crawl_queue:
        # 爬行仍然处于活动状态
        for thread in threads:
            if not thread.is_alive():
                # 移除停止活动的线程
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue:
            # 可以启动更多的线程
            thread = threading.Thread(target=process_queue)
            # 设置进程可以使用ctrl-c 进行退出
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        # 所有的线程都已经被处理
        # 进行休眠
        time.sleep(SLEEP_TIME)

    print("下载完成")
    print("花费时间：" + str(datetime.now() - start_time))


def normalize(seed_url, link):
    """通过删除hash值和添加域来规范化链接"""
    link, _ = urldefrag(link)
    return urljoin(seed_url, link)


def process_link_crawler(args, **kwargs):
    """多进程爬虫"""
    # 获取cpu数量
    num_cpus = multiprocessing.cpu_count()
    print("开始{}个进程".format(num_cpus))
    processes = []

    for i in range(num_cpus):
        # 开始一个新进程，运行函数多线程爬虫函数
        p = multiprocessing.Process(target=threaded_crawler,
                                    args=(args,), kwargs=kwargs)
        p.start()
        processes.append(p)
    # 等待进程执行完毕
    for p in processes:
        # join() 方法实现进程间的同步，等待所有进程退出
        p.join()


if __name__ == '__main__':
    scrape_callback = AlexaCallback()
    process_link_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback,
                     max_threads=5, timeout=10)