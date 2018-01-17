# -*- coding: utf-8 -*-
"""MongoDB 实现缓存"""

import pickle
import zlib
from bson.binary import Binary
from datetime import datetime, timedelta
from pymongo import MongoClient
from 用python写爬虫.复用函数集合 import link_crawler


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


if __name__ == "__main__":
    # url = "https://www.whatismybrowser.com/" \
    #       "developers/what-http-headers-is-my-browser-sending"
    url = 'http://example.webscraping.com'
    link_crawler(url, '/(places/default/index|places/default/view)',
                 max_depth=2, delay=1,
                 max_urls=-1,
                 cache=MongoCache())