# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import string


def clean_input(input):
    input = input.capitalize()
    input = re.sub('\n+', " ", input)
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    clean_input = []
    input = input.split(" ")
    for item in input:
        item = item.strip(string.punctuation)  # 剔除所有标点符号
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            clean_input.append(item)
    return clean_input


def ngrams(input, n):
    """语言模型n-gram的简单应用函数(本例时2-gram)"""
    input = clean_input(input)
    output = dict()
    for i in range(len(input) - n + 1):
        newNGram = " ".join(input[i:i + n])
        if newNGram in output:
            output[newNGram] += 1
        else:
            output[newNGram] = 1
    return output

html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html, 'html5lib')
content = bsObj.find("div", {"id": "mw-content-text"}).get_text()
ngrams = ngrams(content, 2)
ngrams = OrderedDict(sorted(ngrams.items(), key=lambda t: t[1], reverse=True))
print(ngrams)
print("2-grams count is: " + str(len(ngrams)))
