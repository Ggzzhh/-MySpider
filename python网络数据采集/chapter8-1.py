# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
import operator

"""概括数据"""

def is_common(ngram):
    """判断是否常见用语"""
    common_words = ["the", "be", "and", "of", "a", "in", "to", "have", "it",
                    "i", "that", "for", "you", "he", "with", "on", "do", "say",
                    "this", "they", "is", "an", "at", "but", "we", "his",
                    "from", "that", "not", "by", "she", "or", "as", "what",
                    "go", "their", "can", "who", "get", "if", "would", "her",
                    "all", "my", "make", "about", "know", "will", "as", "up",
                    "one", "time", "has", "been", "there", "year", "so",
                    "think", "when", "which", "them", "some", "me", "people",
                    "out", "into", "just", "see", "him", "your", "come",
                    "could", "now", "than", "like", "other", "how", "then",
                    "its", "our", "two", "more", "these", "want", "way", "look",
                    "first", "also", "new", "because", "day", "more", "use",
                    "no", "man", "find", "here", "thing", "give", "many",
                    "well", "take"]
    for word in ngram:
        if word in common_words:
            return True
    return False


def clean_text(input):
    """清理文本"""
    input = re.sub('\n+', ' ', input).lower()
    input = re.sub('\[[0-9]*\]', '', input)
    input = re.sub(' +', ' ', input)
    input = bytes(input, 'UTF-8')
    input = input.decode("utf-8", "ignore")
    return input


def clean_input(input):
    """简单的数据清洗"""
    input = clean_text(input)
    clean_input = []
    input = input.split(" ")
    for item in input:
        item = item.strip(string.punctuation)  # 剔除所有标点符号
        if len(item) > 1 or (item.lower() == 'a' or \
                item.lower() == 'i'):
            clean_input.append(item)
    return clean_input


def ngrams(input, n):
    """获取N元序列排序"""
    input = clean_input(input)
    output = {}
    for i in range(len(input) - n + 1):
        if not is_common(input[i: i+n]):
            ngramTemp = " ".join(input[i: i+n])
            if ngramTemp not in output:
                output[ngramTemp] = 0
            output[ngramTemp] += 1
    return output


content = str(
    urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(),
    'utf-8')
ngrams = ngrams(content, 2)
sortedNGrams = sorted(ngrams.items(), key=operator.itemgetter(1), reverse=True)
print(sortedNGrams)

