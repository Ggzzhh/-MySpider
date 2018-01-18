# -*- coding: utf-8 -*-
"""分布式中的服务端"""
from multiprocessing.managers import BaseManager
from 用python写爬虫.EX4_单独存储队列_MongoDB import MongoQueue


class QueueManage(BaseManager):
    """从BaseManager继承"""
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