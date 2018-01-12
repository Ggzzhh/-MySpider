# -*- coding: utf-8 -*-
"""自动测试同个网站的多个页面"""
import unittest
import re
import random
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import unquote


class TestWikipedia(unittest.TestCase):
    bsObj = None
    url = None

    def test_PageProperties(self):
        global bsObj
        global url

        url = "http://en.wikipedia.org/wiki/Monty_Python"
        # 测试遇到的前100个页面
        for i in range(1, 10):
            bsObj = BeautifulSoup(urlopen(url), 'html5lib')
            titles = self.titleMatchesURL()
            # self.assertEqual(titles[0], titles[1])
            self.assertTrue(self.contentExists())
            url = self.getNextLink()
        print("Done!")

    def titleMatchesURL(self):
        global bsObj
        global url
        pageTitle = bsObj.find("h1").get_text()
        urlTitle = url[(url.index("/wiki/")+6):]
        urlTitle = urlTitle.replace("_", " ")
        urlTitle = unquote(urlTitle)
        return [pageTitle.lower(), urlTitle.lower()]

    def contentExists(self):
        global bsObj
        content = bsObj.find("div", {"id": "mw-content-text"})
        if content is not None:
            return True
        return False

    def getNextLink(self):
        # 使用第五章方法 返回随机链接
        global bsObj
        random.seed(datetime.datetime.now())
        links = bsObj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
        return "http://en.wikipedia.org/" + \
               links[random.randint(0, len(links)-1)].attrs["href"]
