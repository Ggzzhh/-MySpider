# -*- coding: utf-8 -*-
"""
单独存储队列，意味着即使在不同的服务器上的爬虫也能协同处理同一个爬虫任务
实现后就是---分布式爬虫
本文件的单独存储队列基于mongoDB实现
"""

from datetime import datetime, timedelta
from pymongo import MongoClient, errors
from multiprocessing.managers import BaseManager


class MongoQueue:
    # 可能的下载状态
    # 当添加一个新URL时,其状态为OUTSTANDING  0
    # 当URL从队列中取出，未下载时，其状态为PROCESSING  1
    # 下载完成的， 其状态为COMPLETE 2
    OUTSTANDING, PROCESSING, COMPLETE = range(3)

    def __init__(self, client=None, timeout=300):
        self.client = MongoClient() if client is None else client
        self.db = self.client.cache
        self.timeout = timeout

    def __bool__(self):
        """如果有更多的作业要处理， 就返回True"""
        # 查询一个状态不等于COMPLETE的作业
        record = self.db.crawl_queue.find_one(
            {'status': {'$ne': self.COMPLETE}}
        )
        return True if record else False

    def push(self, url):
        """添加一个新url进队列"""
        try:
            # 尝试插入数据
            self.db.crawl_queue.insert(
                {'_id': url, 'status': self.OUTSTANDING}
            )
        except errors.DuplicateKeyError as e:
            pass  # 这已经在队列中了

    def pop(self):
        """
        从队列中获得一个未处理的url把它的状态改为处理中,
        如果队列是空的，就抛出一个KeyError异常
        """
        record = self.db.crawl_queue.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp':
                datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError()

    def peek(self):
        """看一眼运行情况"""
        record = self.db.crawl_queue.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self, url):
        """更新url的状态为已完成"""
        self.db.crawl_queue.update({'_id': url},
                                   {'$set': {'status': self.COMPLETE}})

    def repair(self):
        """
        释放已经超时的作业
        :return: None
        """
        record = self.db.crawl_queue.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.now() - timedelta(
                    seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print('释放：', record['_id'])

    def clear(self):
        """
        清空数据库
        :return: None
        """
        self.db.crawl_queue.drop()


class QueueManage(BaseManager):
    """从basemanage继承"""
    pass


def get_queue():
    queue = MongoQueue()
    return queue


def test():
    # 注册到网上
    QueueManage.register('get_queue', callable=get_queue)

    # 绑定端口5000 设置验证码 'abc'
    manager = QueueManage(address=('', 50000), authkey=65700)
    # 启动
    # manager.start()
    # 通过网络访问
    # 一直启动
    print('服务启动中...')
    s = manager.get_server()
    s.serve_forever()
    # t = manager.get_test()
    # t.clear()
    # t.push('http://www.baidu.com')
    # t.push('http://www.sina.com')
    # t.push('http://www.liaoxuefeng.com')

    # print('尝试获取结果')
    # for i in range(10):
    #     print(r.peek())
    # # 关闭
    # manager.shutdown()

if __name__ == '__main__':
    test()