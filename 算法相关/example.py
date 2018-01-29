# -*- coding: utf-8 -*-
# def create_counter():
#     i = 0
#     def counter():
#         nonlocal i
#         i += 1
#         return i
#     return counter
#
#
# c1 = create_counter()
# print(c1(), c1(), c1(), c1(), c1())


import functools
import time


def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print('%s executed in %s ms' % (fn.__name__, 10.24))
        return fn(*args, **kwargs)
    return wrapper


@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y;


@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z;

f = fast(11, 22)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')