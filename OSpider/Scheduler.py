# -*- coding: utf-8 -*-
import sys
print(sys.path)
import time
import threading
from datetime import datetime
from pprint import pprint

import redis

from OSpider import logger
from OSpider.download import DOWNLOAD
from OSpider.settings import *
"""
    SCHEDULER（调度器）
"""

__author__ = 'Ggzzhh'


class SCHEDULER:
    def __init__(self, callback=None, max_threads=MAX_THREADS,
                 num_retries=NUM_RETRIES, wait_time=5, leave_time=300,
                 **kwargs):
        if hasattr(callback, '__call__'):
            self.callback = callback
        else:
            self.callback = None
        self.wait_time = wait_time
        self.leave_time = leave_time
        self.max_threads = max_threads
        self.num_retries = num_retries
        self.D = DOWNLOAD(**kwargs)
        self.r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                                   socket_keepalive=True, decode_responses=True)
        self.kwargs = kwargs


    def get_url(self):
        """获取url"""
        try:
            if IS_SET_OR_LIST == "SET":
                url = self.r.spop(REDIS_KEY)
            elif IS_SET_OR_LIST == 'LIST':
                url = self.r.lpop(REDIS_KEY)
            else:
                raise ValueError('检查settings文件中IS_SET_OR_LIST的值是否正确')
        except Exception as e:
            logger.error(e)
            return None
        return url

    def crawl(self):
        """抓取流程控制函数"""
        start_time = datetime.now()
        wait = 0
        while True:
            if wait == self.leave_time:
                break
            url = self.get_url()
            if url is None:
                print('抓捕队列为空！等待{}秒后再次尝试！'.format(self.wait_time))
                time.sleep(self.wait_time)
                wait += self.wait_time
                continue
            res = self.D(url, **self.kwargs)
            if self.callback:
                self.callback(response=res)
            else:
                pprint('没有解析函数，直接打印结果：')
                pprint(res)

    def run(self):
        """开始进行抓取"""
        threads = []
        try:
            while True:
                for thread in threads:
                    if not thread.is_alive():
                        # 移除停止活动的线程
                        threads.remove(thread)
                while len(threads) < self.max_threads:
                    break
                print(123)
        except KeyboardInterrupt:
            print('程序停止')
            raise 1


def parse(response):
    print(response)

E = SCHEDULER()
E.run()
