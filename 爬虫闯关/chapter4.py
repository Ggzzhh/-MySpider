# coding=utf-8
import time
import re
from collections import OrderedDict
from datetime import datetime

from threading import Thread
from bs4 import BeautifulSoup

from 爬虫闯关.chapter2 import parse_html
from 爬虫闯关.chapter3 import login

USERNAME = '123312'
PASSWORD = '123123'
login_url = 'http://www.heibanke.com/accounts/login'
seed_url = "http://www.heibanke.com/lesson/crawler_ex03/"
list_url = "http://www.heibanke.com/lesson/crawler_ex03/pw_list"


def get_list(session):
    global PWD
    max_num = -1
    pos = []
    val = []
    index = 0
    for i in range(1, 13):
        res = session.get(list_url + "/?page={}".format(i))
        soup = BeautifulSoup(res.text, 'lxml')
        tds = soup.findAll('td')
        if tds:
            for td in tds:
                if td.has_attr('title'):
                    if td.get('title') == 'password_pos':
                        index = int(td.text) - 1
                        if index > max_num:
                            max_num = index
                    elif td.get('title') == 'password_val':
                        PWD[index] = td.text


def thread_download(target, sleeptime=8, max_threads=15, *args, **kwargs):
    threads = []
    while len(threads) < max_threads:
        new_time = datetime.now()
        print('开始新线程:', new_time)
        for thread in threads:
            if not thread.is_alive():
                print("线程{}结束:{}".format(thread, datetime.now()))
                threads.remove(thread)
        thread = Thread(target=target, args=args, kwargs=kwargs)
        thread.setDaemon(True)
        thread.start()
        threads.append(thread)
        time.sleep(sleeptime)
        print(PWD)
        if ' ' not in PWD:
            break

# while ' ' in PWD:
#     thread_download(get_list, session=session)
#
# print(''.join(PWD))
# print('用时：{}'.format(datetime.now()-now))
with open('test.txt') as f:
    text = f.read()
    res = re.findall('[0-9]', text)
    print(len(res))
    pwd = ''.join(res)
    print(pwd)


session = login()
response = session.get(seed_url)
token = response.cookies['csrftoken']
params = parse_html(response.text)
params['username'] = 'test'
params['password'] = pwd
res = session.post(seed_url, params)
print(res.text)
