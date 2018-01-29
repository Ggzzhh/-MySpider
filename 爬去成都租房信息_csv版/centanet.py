# -*- coding: utf-8 -*-
import threading
import time
import queue

from bs4 import BeautifulSoup
from datetime import datetime

from 爬去成都租房信息_csv版.spider import DownLoad
from 爬去成都租房信息_csv版.models import DiskCache

# 需要收集的信息
FIELDS = []
START_URL = 'http://cd.centanet.com/zufang/g1'
END_URL = 'http://cd.centanet.com/zufang/g35'
SEED_URL = queue.Queue()

for i in range(1, 36):
    SEED_URL.put('http://cd.centanet.com/zufang/g' + str(i))


def thread_crawler(seed_url, scrape_callback=None, max_threads=3, time_sleep=5,
                   cache=None, proxy=False):
    start_time = datetime.now()
    D = DownLoad(proxy=proxy, cache=cache)
    seed_url = seed_url

    def process_queue():
        while not seed_url.empty():
            url = seed_url.get()
            result = D(url)
            if result['code'] == -1:
                print(result['code'])
                # seed_url.put(result['html'])
            else:
                print("网页:{}----下载完毕\n")
            if scrape_callback:
                try:
                    links = scrape_callback(url, result['html']) or []
                except Exception as e:
                    print('回调函数有误: {}---{}'.format(url, e))
                else:
                    print('信息获取完毕\n')

    threads = []
    while threads or not seed_url.empty():
        # 仍然需要爬行
        for thread in threads:
            if not thread.is_alive():
                # 移除停止活动的线程
                threads.remove(thread)
        while len(threads) < max_threads and not seed_url.empty():
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)

        time.sleep(time_sleep)
    print("所有下载已完成")
    print("花费时间：" + str(datetime.now() - start_time))

if __name__ == "__main__":
    thread_crawler(seed_url=SEED_URL, cache=DiskCache(), proxy=True)