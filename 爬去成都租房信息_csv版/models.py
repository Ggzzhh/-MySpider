# -*- coding: utf-8 -*-
from urllib.request import urlparse, urlopen
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from 爬去成都租房信息_csv版.c_ip import get_ips, del_ip
import requests
import time
import os
import hashlib
# 保持打开状态
import pickle
# 压缩以及解压
import zlib
import csv
import re


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


class CentCallback:
    """中原成都租房网"""
    def __init__(self):
        self.writer = csv.writer(open('tenement.csv', 'a', encoding='utf-8'))

    def __call__(self, url, html):
        if re.search('centanet', url):
            soup = BeautifulSoup(html, 'lxml')
            domain = urlparse(url).netloc
            lists = soup.find_all('div', class_='house-item')
            for list in lists:
                row = []
                # 总览
                infos = list.find('p', class_='listButton')\
                    .find('a', class_='js_contrast')
                # 房源名
                row.append(infos.attrs['data-title'])
                # 网址
                row.append(domain + infos.attrs['data-url'])
                # 小区名
                row.append(infos.attrs['data-estatename'])
                # 户型
                row.append(infos.attrs['data-housetype'])
                # 面积
                row.append(infos.attrs['data-garea'])
                # 价格
                price = list.find('p', class_='price-nub').span.text
                row.append(price)
                house_txts = list.find_all('p', class_='house-txt')
                # 面积 朝向 楼层 装修 建造时间 出租类型
                txts = house_txts[0].get_text().strip().split('|')
                for txt in txts:
                    row.append(txt)
                # 所在区 地址
                district = house_txts[1].text.strip().split('-')
                row.append(district[0])
                row.append(district[1])
                # 标签
                flags = list.find('p', class_='labeltag').find_all('span')
                temp = ''
                for flag in flags:
                    temp += (flag.text + ' ')
                row.append(temp)

                self.writer.writerow(row)


class FTXCallback:
    """房天下网 未完成"""
    def __init__(self):
        self.writer = csv.writer(open('tenement.csv', 'a'))

    def __call__(self, url, html):
        if re.search('fang', url):
            html = html.encode(encoding='UTF-8', errors='ignore')
            soup = BeautifulSoup(html, 'lxml')
            print(soup)
            domain = urlparse(url).netloc
            lists = soup.find_all('dl', class_='list')
            print(lists)
            for list in lists:
                row = []
                list = list.find('dd', class_='info')
                # 房源名
                name = list.find('p', class_='title').a
                row.append(name.text)
                # 网址
                row.append(domain + name.attrs['href'])

                infos = list.select("p[class='gray6 mt20']").find_all('a')
                infos_2 = list.find("p", class_='font16 mt20 bold').get_text(
                    '|', strip=True)
                # 小区名
                row.append(infos[2].get_text(strip=True))
                # 户型

                # 面积

                # 价格
                price = list.find('p', class_='price-nub').span.text
                row.append(price)
                house_txts = list.find_all('p', class_='house-txt')
                # 朝向 楼层 装修 建造时间 出租类型
                txts = house_txts[0].get_text().strip().split('|')
                for txt in txts:
                    row.append(txt)
                # 所在区 地址
                district = house_txts[1].text.strip().split('-')
                row.append(district[0])
                row.append(district[1])
                # 标签
                flags = list.find('p', class_='labeltag').find_all('span')
                temp = ''
                for flag in flags:
                    temp += (flag.text + ' ')
                row.append(temp)
                print(row)
                # self.writer.writerow(row)


class AJKCallback:
    """安居客"""
    def __init__(self):
        self.writer = csv.writer(open('tenement.csv', 'a', encoding='utf-8'))

    def __call__(self, url, html):
        if re.search('anjuke', url):
            soup = BeautifulSoup(html, 'lxml')
            domain = urlparse(url).netloc
            lists = soup.find_all('div', class_='zu-itemmod')
            for txt in lists:
                row = []
                # 总览
                list = txt.find('div', class_='zu-info')
                # 房源名
                row.append(list.h3.get_text(strip=True))
                # 网址
                row.append(list.h3.a.attrs['href'])
                # 小区名
                add = list.find('address')
                row.append(add.a.text.strip())
                # 户型
                items = list.find_all('p', class_='details-item')
                infos = items[0].get_text(strip=True).split("|")
                row.append(infos[0])
                # 面积
                area = re.search('[0-9]+', infos[1])
                if area:
                    row.append(area.group())
                # 价格
                price = txt.find('div', class_='zu-side').p.strong.text
                row.append(price)
                # 朝向
                infos_2 = items[1].find_all('span')
                row.append(infos_2[1].text)
                # 楼层
                row.append(infos[2])
                # 装修
                row.append(' ')
                # 建造时间
                row.append(' ')
                # 出租类型
                row.append(infos_2[0].text)
                # 所在区 地址
                district = add.get_text().strip().split('\n')[1].split('-')
                row.append(district[0].strip())
                row.append(district[1])
                # 标签
                flags = infos_2[2:]
                if flags:
                    x = ''
                    for i in flags:
                        x += i.text + ' '
                    row.append(x)
                else:
                    row.append(' ')
                # print(row)
                self.writer.writerow(row)


class Five8Callback:
    """58同城  不包括58品质租房"""
    def __init__(self):
        self.writer = csv.writer(open('tenement.csv', 'a',
                                      encoding='utf-8'))

    def __call__(self, url, html):
        if re.search('58', url):
            soup = BeautifulSoup(html, 'lxml')
            links = soup.find('ul', class_='listUl').find_all('a')
            used = []
            for link in links:
                href = link.attrs['href']
                if self.we_need(href) and href not in used:
                    used.append(href)
            return list(set(used))

    @staticmethod
    def we_need(url):
        """检验是否是我们需要的url"""
        parse = urlparse(url)
        if parse.netloc == 'jxjump.58.com' and parse.path == '/service':
            return True
        if parse.netloc == 'cd.58.com':
            if re.search('zufang', parse.path) and 'pn' not in parse.path:
                if len(parse.path) > 7:
                    return True
        if parse.netloc == 'short.58.com':
            return True
        return False


class FiveECallback:
    """解析具体页面并添加至tenement.csv"""

    def __init__(self):
        self.writer = csv.writer(open('tenement.csv', 'a', encoding='utf-8'))

    def __call__(self, url, html):
        row = []
        if re.search('58', url):
            bs = BeautifulSoup(html, 'lxml')
            # 房源名
            name = bs.find('div', class_='house-title')
            row.append(name.h1.text)
            # 网址
            parse = urlparse(url)
            row.append((parse.scheme + '://' + parse.netloc +
                        parse.path).strip())
            # 小区名
            basic = bs.find('div', class_='house-desc-item') \
                .find('ul', class_='f14').find_all('li')
            row.append(basic[3].a.text)
            # 户型
            txt1 = basic[1].find_all('span')[1].get_text(
                strip=True).split(' ')
            txt1 = [i.strip() for i in txt1 if i]
            row.append(txt1[0])
            # 面积
            row.append(txt1[1])
            # '价格'
            row.append(
                bs.find('div', class_='house-pay-way').span.b.text
            )
            # '朝向'
            txt2 = basic[2].find_all('span')[1].get_text(
                strip=True).split('\xa0')
            row.append(txt2[0])
            # '楼层'
            row.append(txt2[-1])
            # '装修'
            row.append(txt1[-1])
            # '建造时间'
            row.append(' ')
            # '出租类型'
            row.append(basic[0].find_all('span')[-1].text)
            # '所在区'
            txt3 = basic[4].find_all('a')
            row.append(txt3[0].text)
            # '地址'
            row.append(txt3[1].text)
            # '标签'
            row.append(' ')
            # print(row)
            self.writer.writerow(row)
            time.sleep(3)


class GanJiCallback:
    """赶集网成都租房"""
    def __init__(self):
        self.writer = csv.writer(open('tenement.csv', 'a', encoding='utf-8'))

    def __call__(self, url, html):
        if re.search('ganji', url):
            soup = BeautifulSoup(html, 'lxml')
            domain = urlparse(url).netloc
            lists = soup.find_all('div', class_='f-list-item')
            for list in lists:
                row = []
                # 总览
                list = list.find('dl', class_='f-list-item-wrap')
                # 房源名
                name = list.find('dd', class_='title').a
                row.append(name.text)
                # 网址
                row.append((domain + name.attrs['href']).strip())
                # 小区名
                address = list.find('dd', class_='address').find_all('a')
                row.append(address[-1].text)
                # 户型
                sizes = list.find('dd', class_='size').find_all('span')
                size = sizes[0].text
                if size == '整租':
                    row.append(sizes[2].text)
                else:
                    continue
                # 面积
                ans = re.search("[0-9]+", sizes[4].text)
                if ans:
                    row.append(ans.group())
                else:
                    row.append(' ')
                # 价格
                price = list.find('dd', class_='info').find('div', 'price')\
                    .find('span', 'num').get_text()
                try:
                    price = int(price)
                except Exception as e:
                    continue
                else:
                    if price > 1000:
                        row.append(price)
                    else:
                        continue
                # 朝向
                if len(sizes) > 10:
                    row.append(sizes[6].get_text(strip=True))
                # 楼层
                    row.append(sizes[8].get_text(strip=True))
                # 装修
                    row.append(sizes[-1].get_text(strip=True))
                # 建造时间
                    row.append(' ')
                # 出租类型
                    row.append(size)
                # 所在区
                row.append(address[0].get_text(strip=True))
                # 地址
                row.append(address[1].get_text(strip=True))
                # 标签
                flag = list.find('dd', 'feature').get_text(' ', strip=True)
                row.append(flag)
                # print(row)
                self.writer.writerow(row)


class GetLianJiaUrl:
    """收集链家所有租房信息url"""
    def __init__(self):
        self.writer = csv.writer(open('tenement.csv', 'a',
                                      encoding='utf-8'))

    def __call__(self, url):
        driver = webdriver.PhantomJS(
            executable_path=r"D:\Web\phantomjs-2.1.1-windows\bin\phantomjs.exe")
        driver.get(url)
        time.sleep(5)
        links = driver.find_element_by_id('house-lst').find_elements_by_xpath(
            '//h2/a')
        lists = []
        for link in links:
            lists.append(link.get_property('href'))
        return lists


class LianJiaCallback:
    """提取链家网页中的信息"""
    def __init__(self):
        self.writer = csv.writer(open('tenement.csv', 'a', encoding='utf-8'))

    def __call__(self, url, html):
        if re.search('lianjia', url):
            row = []
            soup = BeautifulSoup(html, 'lxml')
            content = soup.find('div', class_='content-wrapper')
            title = content.find('div', class_='title-wrapper').div.find(
                'div', class_='title')
            overview = content.find('div', class_='overview')\
                .find('div', class_='content')
            room = overview.find('div', class_='zf-room').find_all('p')
            price = overview.find('div', class_='price')
            if len(room) != 8:
                raise 'index 出现错误'
            # 房源名'
            row.append(title.h1.get_text(strip=True))
            # '网址'
            row.append(url)
            # '小区名'
            row.append(room[5].a.get_text(strip=True))
            # 户型
            x = ''
            for y in room[1].stripped_strings:
                x = y
            x = x.split(' ')
            row.append(x[0])
            # 面积
            row.append(room[0].get_text(strip=True).split('：')[-1])
            # '价格'
            row.append(price.find('span', class_='total').get_text(strip=True))
            # '朝向'
            row.append(room[3].get_text(strip=True).split('：')[-1])
            # '楼层'
            row.append(room[2].get_text(strip=True).split('：')[-1])
            # '装修'
            zx = price.find('span', class_='tips')
            row.append(zx.get_text(strip=True) if zx else '空')
            # '建造时间'
            row.append(' ')
            # '出租类型'
            row.append(x[-1])
            # '所在区'
            address = room[6].find_all('a')
            row.append(address[0].get_text(strip=True))
            # '地址'
            row.append(address[-1].get_text(strip=True))
            # '标签'
            row.append(title.find('div', class_='sub').get_text(strip=True))
            # print(row)
            self.writer.writerow(row)

FIELD = ('房源名', '网址', '小区名', '户型', '面积', '价格', '朝向', '楼层', '装修',
         '建造时间', '出租类型', '所在区', '地址', '标签')
if __name__ == '__main__':
    # 户型
    # 面积
    # '价格'
    # '朝向'
    # '楼层'
    # '装修'
    # '建造时间'
    # '出租类型'
    # '所在区'
    # '地址'
    # '标签'
    # cache = DiskCache()
    url = 'https://cd.lianjia.com/zufang/106100943871.html'
    session = requests.Session()
    html = session.get(url).text
    lian = LianJiaCallback()
    lian(url, html)

    # print(html)
    # test = GanJiCallback()
    # test(url, html)
