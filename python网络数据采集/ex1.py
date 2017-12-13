# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "html5lib")

# nameList = bsObj.findAll("span", {"class": "green"})
# for name in nameList:
#     print(name.get_text())

# for child in bsObj.find("table",{"id":"giftList"}).children:
#     print(child)

# 正则和Bs4
images = bsObj.findAll("img",
                       {
                           # 以../img/gifts开头 以.jpg结尾的图片
                           "src": re.compile("\.\.\/img\/gifts/img.*\.jpg")
                       })
for image in images:
    print(image["src"])
