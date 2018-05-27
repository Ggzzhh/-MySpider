try:
    import OSpider
except:
    import sys
    import os
    sys.path.append(os.path.abspath('..'))
import redis
import json
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from OSpider import OSPIDER


class T(OSPIDER):
    def parse(self, response):
        soup = BeautifulSoup(response['html'], 'lxml')
        find = soup.find('div', {"class": 'bookname'}).h1
        print(find)


if __name__ == '__main__':
    t = T()
    t.run()