# -*- coding: utf-8 -*-
import time
import threading
from datetime import datetime
from pprint import pprint

import redis

try:
    import OSpider
except:
    import sys
    import os
    sys.path.append(os.path.abspath('..'))

from OSpider import logger
from OSpider.download import DOWNLOAD
from OSpider.settings import *

"""
    SCHEDULER（调度器）
"""

__author__ = 'Ggzzhh'


class SCHEDULER:
    def __init__(self, callback=None, max_threads=MAX_THREADS,
                 wait_time=WAIT_TIME, leave_time=LEAVE_TIME, **kwargs):
        """

        :param callback:  需要一个接受response实参的函数作为回调，像这样
                          def parse(response):
                              pass
        :param max_threads: 最大线程数
        :param wait_time: 当队列为空时，等待几秒之后继续抓取。
        :param leave_time: 累计等待多久中断程序
        :param kwargs: 。。。
        """
        if hasattr(callback, '__call__'):
            self.callback = callback
        else:
            self.callback = None
        self.wait_time = wait_time
        self.leave_time = leave_time
        self.max_threads = max_threads
        self.D = DOWNLOAD(**kwargs)
        self.r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                                   socket_keepalive=True, decode_responses=True)
        self.kwargs = kwargs
        self.start_num = self.show_num()
        self.start_time = datetime.now()

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
        while True:
            if self.leave_time == 0:
                break
            url = self.get_url()
            if url is None:
                break
            res = self.D(url, **self.kwargs)
            if self.callback:
                self.callback(response=res)
            else:
                pprint('没有解析函数，直接打印结果：')
                pprint(res)

    def run(self):
        """开始进行抓取"""
        threads = []
        wait = 0
        try:
            while True:
                num = self.show_num()
                if num is None or num == 0:
                    print('抓捕队列为空！{}秒后继续抓取'.format(self.wait_time))
                    time.sleep(self.wait_time)
                    wait += self.wait_time
                    if wait >= self.leave_time:
                        print('{}秒内获取不到url，程序终端'.format(self.leave_time))
                        break
                    continue
                for thread in threads:
                    if not thread.is_alive():
                        # 移除停止活动的线程
                        threads.remove(thread)
                while len(threads) < self.max_threads:
                    thread = threading.Thread(target=self.crawl)
                    thread.setDaemon(True)
                    thread.start()
                    threads.append(thread)
                time.sleep(3)
        except KeyboardInterrupt:
            self.leave_time = 0
            for thread in threads:
                thread.join()
                if thread.is_alive():
                    threads.remove(thread)
            print('程序停止!')
            print('花费时间{}'.format(datetime.now() - self.start_time))
            print('下载了{}个url的内容'.format(self.start_num - self.show_num()))

    def show_num(self):
        """
        :return: 给定的KEY值的数量
        """
        try:
            if IS_SET_OR_LIST == "SET":
                num = self.r.scard(REDIS_KEY)
            elif IS_SET_OR_LIST == 'LIST':
                num = self.r.llen(REDIS_KEY)
            else:
                raise ValueError('检查settings文件中IS_SET_OR_LIST的值是否正确')
        except Exception as e:
            logger.error(e)
            return 0
        return num or 0

