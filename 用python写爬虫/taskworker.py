# -*- coding: utf-8 -*-
"""分布式任务的工作者"""
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


def test_1():
    # 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
    QueueManager.register('get_queue')

    server_addr = '192.168.1.128'
    print('连接至', server_addr)

    m = QueueManager(address=(server_addr, 50000), authkey=65700)
    try:
        m.connect()
    except Exception as e:
        print("出现错误：", e)
    else:
        print('链接成功...')
    task = m.get_queue()
    task.push('http://www.baidu.com')
    print('放置成功')
    print(task.peek())

if __name__ == '__main__':
    test_1()



