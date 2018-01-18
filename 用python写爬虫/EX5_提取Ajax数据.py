# -*- coding: utf-8 -*-
"""
Ajax搜索脚本
服务端并没有检查该参数是否与 界面允许 的选项值相 匹 配 ， 而是直
接在一个页面 中 返 回 了 所有结果 。 许多 Web 应用 不会在 AJAX 后端检查这一
参数 ， 因 为 它们认为 请求只 会来 自 Web 界面
"""

import json
import string
import time

from 用python写爬虫.复用函数集合 import DownLoader


template_url = "http://example.webscraping.com/places/ajax/search.json" \
               "?&search_term=.&page_size=1000&page=0"
# 用来存储已经收藏过的国家
countries = set()

D = DownLoader()

html = D(template_url)
try:
    ajax = json.loads(html)
except ValueError as e:
    print(e)
    ajax = None
else:
    for record in ajax['records']:
        countries.add(record['country'])

print(countries)
