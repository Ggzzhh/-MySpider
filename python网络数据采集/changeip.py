# coding=utf-8
from stem import Signal
from stem.control import Controller
import socket
import socks
import requests
import time
import sys

controller = Controller.from_port(port=9151)
controller.authenticate()
socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket

total_scrappy_time = 0
total_changeIP_time = 0
for x in range(0, 10):
    a = requests.get("http://checkip.amazonaws.com").text
    print("第" + str(x + 1) + "次IP：" + a)

    time1 = time.time()
    a = requests.get("http://www.santostang.com/").text

    time2 = time.time()
    total_scrappy_time = total_scrappy_time + time2 - time1
    print("第" + str(x + 1) + "次抓取花费时间：" + str(time2 - time1))

    time3 = time.time()
    controller.signal(Signal.NEWNYM)
    time.sleep(5)
    time4 = time.time()
    total_changeIP_time = total_changeIP_time + time4 - time3 - 5
    print("第" + str(x + 1) + "次更换IP花费时间: " + str(time4 - time3 - 5))

print("平均抓取花费时间：" + str(total_scrappy_time / 10))
print("平均更换IP时间：" + str(total_changeIP_time / 10))