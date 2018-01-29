# -*- coding: utf-8 -*-
from urllib.request import urlparse
from datetime import datetime, timedelta
import time
import os
import hashlib
# 保持打开状态
import pickle
# 压缩以及解压
import zlib


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