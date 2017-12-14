# -*- coding: utf-8 -*-
import re
import datetime
import random

from urllib.request import urlopen
from urllib.request import urlparse
from bs4 import BeautifulSoup


# 获取页面所有内链的列表
def get_internal_links(bs_obj, include_url):
    """获取内链列表 参数1: 需要bs对象 参数2 需要bs对象的url"""
    parse = urlparse(include_url)
    if parse.netloc != '':
        include_url = urlparse(include_url).scheme + "://" + urlparse(
            include_url).netloc
    internal_links = []
    # 找出所有以“/”或者页面本身开头的链接
    for link in bs_obj.findAll("a", href=re.compile("^(/|.*"+include_url+")")):
        if link.attrs["href"] is not None:
            if link.attrs['href'] not in internal_links:
                internal_links.append(link.attrs['href'])
    return internal_links


# 获取页面所有的外部链接列表
def get_external_links(bs_obj, exclude_url):
    """获取外链列表 参数1: 需要bs对象 参数2 排除对象url"""
    parse = urlparse(exclude_url)
    if parse.netloc != '':
        exclude_url = parse.netloc
    external_links = []
    for link in bs_obj.findAll("a", href=re.compile(
                            "^(http|www)((?!"+exclude_url+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_links:
                external_links.append(link.attrs['href'])
    return external_links


# 收集网站上的所有外链
# todo：写入数据库或者excel的函数 暂时用set()列表代替
all_ext_links = set()  # 所有外链
all_int_links = set()  # 所有内链


def get_all_external_links(site_url):
    """接收一个网址 返回该网址所有外链"""
    try:
        html = urlopen(site_url)
        domain = urlparse(site_url).scheme + "://" + urlparse(site_url).netloc
        bs_obj = BeautifulSoup(html, 'html5lib')
    except Exception as e:
        print("发生错误：%s\n" % e)
        return "url错误"
    internal_links = get_internal_links(bs_obj, domain)
    external_links = get_external_links(bs_obj, domain)

    for link in external_links:
        if link not in all_ext_links:
            all_ext_links.add(link)
            print(link)
    for link in internal_links:
        if link not in all_int_links:
            print("即将在：%s 页面获取url" % link)
            all_int_links.add(link)
            get_all_external_links(link)


result = get_all_external_links("http://www.pdsu.edu.cn/")
print(all_ext_links)
print('内链：')
print(all_int_links)