# -*- coding: utf-8 -*-
"""修改请求头 headers 使用requests模块进行自定义headers"""

import requests
from bs4 import BeautifulSoup

session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/63.0.3239.132 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;"
                     "q=0.9,image/webp,image/apng,*/*;q=0.8"
           }
url = "https://www.whatismybrowser.com/" \
      "developers/what-http-headers-is-my-browser-sending"
req = session.get(url, headers=headers)

bsObj = BeautifulSoup(req.text, "html5lib")
print(bsObj.find("table", {"class": "table-striped"}).get_text)
