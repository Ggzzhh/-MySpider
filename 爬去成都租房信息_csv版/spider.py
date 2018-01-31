# -*- coding: utf-8 -*-
import threading
import time
import queue

from bs4 import BeautifulSoup
from datetime import datetime

from 爬去成都租房信息_csv版.download import DownLoad
from 爬去成都租房信息_csv版.models import DiskCache, CentCallback, AJKCallback, \
    Five8Callback, FiveECallback, GanJiCallback

# 需要收集的网站队列
SEED_URL = queue.Queue()

# 房天下 动态加载  需要另写
# for i in range(1, 101):
#     SEED_URL.put('http://zu.cd.fang.com/house/i3'.format(str(i)))

# 中原成都租房网
# for i in range(1, 35):
#     SEED_URL.put('http://cd.centanet.com/zufang/g{}'.format(str(i)))

# 58
# for i in range(1, 71):
#     SEED_URL.put('http://cd.58.com/zufang/pn{}/'.format(str(i)))
# with open('ips.txt') as f:
#     temp = set()
#     for i in f:
#         temp.add(i)
# # 共1902
# for i in temp:
#         SEED_URL.put(i)

# 赶集 http://cd.ganji.com/fang1/m1o87/
for i in range(1, 88):
    SEED_URL.put('http://cd.ganji.com/fang1/m1o{}/'.format(str(i)))

# 安居客
# for i in range(1, 50):
#     SEED_URL.put('https://cd.zu.anjuke.com/fangyuan/p{}-x1/'.format(str(i)))

# 链家 https://cd.lianjia.com/zufang/pg100/
# for i in range(1, 101):
#     SEED_URL.put('https://cd.lianjia.com/zufang/pg{}/'.format(str(i)))

# 百姓网 http://chengdu.baixing.com/zhengzu/m37617/?page=100
# for i in range(1, 101):
#     SEED_URL.put('http://chengdu.baixing.com/zhengzu/m37617/?page={}'.format(
#         str(i)))


def thread_crawler(seed_url, scrape_callback=None, max_threads=15, time_sleep=3,
                   cache=None, proxy=False):
    start_time = datetime.now()
    D = DownLoad(proxy=proxy, cache=cache)
    seed_url = seed_url

    def process_queue():
        while not seed_url.empty():
            url = seed_url.get()
            result = D(url)
            if result == '':
                print("无内容！添加{}".format(url))
                D.num_retries += 3
                seed_url.put(url)
            else:
                print("网页:{}----下载完毕\n".format(url))
                seed_url.task_done()
                if scrape_callback:
                    try:
                        links = scrape_callback(url, result) or []
                    except Exception as e:
                        print('回调函数有误: {}---{}'.format(url, str(e)))
                    else:
                        if links is not []:
                            with open('ips.txt', 'a') as f:
                                for link in links:
                                    f.write(link + '\n')
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
    thread_crawler(seed_url=SEED_URL, cache=DiskCache(),
                   proxy=True, scrape_callback=GanJiCallback())