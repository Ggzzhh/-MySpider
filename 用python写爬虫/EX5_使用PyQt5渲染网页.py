# -*- coding: utf-8 -*-
"""如题"""
import sys
from bs4 import BeautifulSoup
from 用python写爬虫.复用函数集合 import DownLoader
# 导入需要的库？？？
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

D = DownLoader()

url = 'http://example.webscraping.com/places/default/dynamic'
# html = D(url)


class WebRender(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.loadFinished.connect(self.__loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def __loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

r = WebRender(url)
html = r.frame.toHtml()
print(html)