# -*- coding: utf-8 -*-
"""
单独存储队列，意味着即使在不同的服务器上的爬虫也能协同处理同一个爬虫任务
实现后就是---分布式爬虫
本文件的单独存储队列基于mongoDB实现
"""

from datetime import datetime, timedelta
from pymongo import MongoClient, errors

class MongoQueue:
    # 可能的下载状态
    # 当添加一个新URL时,其状态为OUTSTANDING  0
    # 当URL从队列中取出，未下载时，其状态为PROCESSING  1
    # 下载完成的， 其状态为COMPLETE 2
    OUTSTANDING, PROCESSING, COMPLETE = range(3)