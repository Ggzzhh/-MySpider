# -*- coding: utf-8 -*-
import os
import re
import time
from datetime import datetime
from random import random
from pprint import pprint
from urllib.request import urlretrieve
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse, urldefrag, urlsplit

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

DELAY = 2
DOMAINS_TIME = {}
HEADERS = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 '
                  'Firefox/38.0 Iceweasel/38.3.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive'
}
PROXIES = {}
DEFAULT_TIMEOUT = 10
THREAD_NUM = 20

MONGODB = MongoClient()
DB = MONGODB.The163


def get_delay():
    """获取一个基础等待时常加一个随机数"""
    return DELAY + random()


def get_id(str):
    """筛选出网易音乐中的各种id"""
    if str:
        id_ = re.search('id=(\d+)', str)
        if id_:
            return id_.groups()[0]
    return


def music2disk(music_name, music_id, path=""):
    """
    将音乐下载到本地
    :param music_name: 歌曲名
    :param music_id: 歌曲在网易云的id
    :param path: 保存地址，默认为当前文件夹下的music文件夹
    :return: 成功 或者 失败  True or False
    """
    download_url = "http://music.163.com/song/media/outer/url?id={music_id}.mp3"
    if path is "":
        path = os.getcwd() + "\\music"
        if not os.path.exists(path):
            os.mkdir(path)
    filename = path + "\\" + music_name + music_id + ".mp3"
    filename = re.sub(' ', '_', filename)
    if os.path.exists(filename):
        print('《{}》已存在, '.format(music_name))
        return True
    try:
        urlretrieve(download_url.format(music_id=music_id), filename)
    except Exception as e:
        print("出现错误：")
        print(e)
        return False
    else:
        return True


def download(url, headers=HEADERS, proxies=PROXIES, timeout=DEFAULT_TIMEOUT):
    """
    下载器
    :param url:  下载地址
    :param headers:  下载时使用的头信息
    :param proxies:  下载时使用的代理信息
    :param timeout:  获取页面时的时间超时判断,单位为s
    :return: 返回一个response对象 或者 None
    """
    s = requests.Session()
    try:
        response = s.get(url, headers=headers, proxies=proxies, timeout=timeout)
    except Exception as e:
        pprint('出现错误: {}'.format(e))
        return None
    else:
        return response


def get_playlist(url='', page_count=1):
    """
    获取所有热门歌单的id 并将歌单名和收听人数一起写入mongodb中
    :return: None

    """

    collecotion = DB.playlists

    base_url = "http://music.163.com"
    seed_url = "/discover/playlist/?order=hot&cat=%E5%85" \
               "%A8%E9%83%A8&limit=35&offset=0"
    if url is "":
        url = base_url + seed_url
    else:
        url = base_url + url
    res = download(url)
    if res and res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        ul = soup.find('ul', class_='m-cvrlst')
        lis = ul.find_all('li')
        for li in lis:
            playlist = dict()
            playlist['name'] = li.a['title']
            playlist['play_num'] = li.find('span', class_='nb').text
            id_ = get_id(li.a['href'])
            if id_:
                collecotion.update({'_id': id_}, {"$set": playlist}, True)
        print('第{page_count}页: {url} 完成!'.format(page_count=page_count,
                                                 url=url))
        next_url = soup.find('a', class_='znxt')
        if next_url['href'] != 'javascript:void(0)':
            delay = get_delay()
            print('请等待{}秒'.format(delay))
            time.sleep(delay)
            get_playlist(next_url['href'], page_count+1)
        else:
            count = collecotion.count()
            print('运行结束！一共{}个歌单保存完毕!'.format(count))


def get_music_id(url):
    """
    获取url(歌单url或者某歌手主页的url)当中的所有歌曲id
    :param url:
    :return: 歌单字典
    """
    songs = dict()
    res = download(url)
    if res and res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        links = soup.select('ul[class="f-hide"] > li > a')
        if not links:
            raise ValueError('404了！url错误!')
        for a in links[72:]:
            id_ = get_id(a['href'])
            name = a.text
            if id_ and name:
                DB.music.update({'_id': id_}, {"$set": {'name': name}}, True)
                print("歌曲{}已入库！".format(name))
                songs[name] = id_
    return songs


def download_music(music_name, music_id=None, path=''):
    """下载某歌曲到本地（目前无法区分是哪个版本）"""
    t = datetime.now()
    if music_id:
        song = DB.music.find_one({'_id': music_id})
    else:
        rexEXP = re.compile(r'^{}.*'.format(music_name))
        song = DB.music.find_one({'name': rexEXP})
    if song:
        music2disk(song['name'], song['_id'], path)
    else:
        print("未找到该歌曲！")
    return

if __name__ == "__main__":
    music_name = '阳光彩虹小白马'
    music_id = '551339740'
    print(music2disk(music_name, music_id))
    # get_playlist()
    # douyin = get_music_id('http://music.163.com/playlist?id=2183461281')
    # for key, value in douyin.items():
    #     download_music(key, music_id=value)
    #     time.sleep(get_delay())
