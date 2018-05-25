# -*- coding: utf-8 -*-
"""
默认设置
"""
# 日志级别
LEVEL = 'DEBUG'
# 默认下载间隔
DELAY = 0.5
# 等待超时
TIMEOUT = 30
# 使用的头信息
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 '
                  'Firefox/38.0 Iceweasel/38.3.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
}
# 最大线程
MAX_THREADS = 10
# 重试次数
NUM_RETRIES = 3
# 代理池
PROXY = {
    'https': '36.68.68.77:3128'
}
# 队列为空时等待多久后再次尝试
WAIT_TIME = 3
# 队列为空时总等待时常，超时中断程序
LEAVE_TIME = 30
# redis相关设置
REDIS_HOST = '127.0.0.1'
# redis服务器端口
REDIS_PORT = '6379'
# url所在的key
REDIS_KEY = 'zhihu'
# 使用list存储还是set 默认为LIST 可改为SET
IS_SET_OR_LIST = 'SET'


