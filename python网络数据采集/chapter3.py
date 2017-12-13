# -*- coding: utf-8 -*-
import re
import random
import datetime

from bs4 import BeautifulSoup
from urllib.request import urlopen

"""第三章 开始采集"""

# html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
# bsObj = BeautifulSoup(html, "html5lib")
#
# for link in bsObj.find("div", {"id": "bodyContent"})\
#         .findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
#     if "href" in link.attrs:
#         print(link.attrs['href'])

# 更换当前随机数的种子
# random.seed(datetime.datetime.now())
#
#
# def get_links(article_url):
#     html = urlopen("http://en.wikipedia.org" + article_url)
#     bs_obj = BeautifulSoup(html, "html5lib")
#     return bs_obj.find("div", {"id": "bodyContent"}) \
#         .findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
#
# links = get_links("/wiki/Kevin_Bacon")
# while len(links) > 0:
#     new_article = links[random.randint(0, len(links) - 1)].attrs["href"]
#     print(new_article)
#     links = get_links(new_article)


# # 遍历整个网站
# pages = set()
# pages.add("http://www.hapds.lss.gov.cn")
# links = ["http://www.hapds.lss.gov.cn"]
#
#
# def get_links(page_url):
#     """爬取平顶山人事网"""
#     global pages
#     html = urlopen(page_url)
#     bs_obj = BeautifulSoup(html, "html5lib")
#
#     try:
#         print(bs_obj.find("div", {"class": "c-tittle"}).get_text())
#     except AttributeError:
#         print("缺少标题属性")
#
#     for link in bs_obj.findAll("a", href=re.compile(
#             "^http://www\.hapds\.lss\.gov\.cn((/.)*).*\.html$")):
#         if 'href' in link.attrs:
#             if link.attrs['href'] not in pages:
#                 # 新页面
#                 new_page = link.attrs['href']
#                 # print(new_page)
#                 pages.add(new_page)
#                 links.append(new_page)
#
# while len(links) > 0:
#     try:
#         page = links.pop()
#         get_links(page)
#     except Exception as e:
#         print(page + '打开页面出现异常')
#         print(e)



