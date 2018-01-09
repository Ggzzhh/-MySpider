# -*- coding: utf-8 -*-
# 简单的马尔可夫模型

from urllib.request import urlopen
from random import randint


def word_list_sum(word_list):
    """计算单词出现的次数"""
    sum = 0
    for word, value in word_list.items():
        sum += value
    return sum


def retrieve_random_word(word_list):
    """随机检索单词"""
    rand_index = randint(1, word_list_sum(word_list))
    # print('rand_index1: %s' % rand_index)
    for word, value in word_list.items():
        # print(word, value)
        rand_index -= value
        # print('rand_index2: %s' % rand_index)
        if rand_index <= 0:
            return word


def build_word_dict(text):
    """根据文本建设单词字典"""
    # 剔除换行符和引号
    text = text.replace("\n", " ")
    text = text.replace("\"", "")

    # 保证每个标点符号都和前面的单词在一起
    # 这样不会被剔除，保留在马尔可夫链中
    punctuation = [',', '.', ';', ':', '，', '。']
    for symbol in punctuation:
        text = text.replace(symbol, " " + symbol + " ")

    words = text.split(" ")
    # 过滤空单词
    words = [word for word in words if word != ""]

    word_dict = {}

    for i in range(1, len(words)):
        if words[i-1] not in word_dict:
            # 为单词新建一个词典
            word_dict[words[i-1]] = {}
        if words[i] not in word_dict[words[i-1]]:
            word_dict[words[i-1]][words[i]] = 0
        word_dict[words[i-1]][words[i]] = word_dict[words[i-1]][words[i]] + 1

    return word_dict

text = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt"
                   "").read(), 'utf-8')
text = """由于Python语言的简洁性、易读性以及可扩展性，在国外用Python做科学计算的研究机构日益增多，一些知名大学已经采用Python来教授程序设计课程。例如卡耐基梅隆大学的编程基础、麻省理工学院的计算机科学及编程导论就使用Python语言讲授。众多开源的科学计算软件包都提供了Python的调用接口，例如著名的计算机视觉库OpenCV、三维可视化库VTK、医学图像处理库ITK。而Python专用的科学计算扩展库就更多了，例如如下3个十分经典的科学计算扩展库：NumPy、SciPy和matplotlib，它们分别为Python提供了快速数组处理、数值运算以及绘图功能。因此Python语言及其众多的扩展库所构成的开发环境十分适合工程技术、科研人员处理实验数据、制作图表，甚至开发科学计算应用程序。"""
word_dict = build_word_dict(text)
# print(word_dict)
# 生成链长为100的马尔可夫链
length = 100
chain = ""
current_word = "由于Python语言的简洁性、易读性以及可扩展性"
for i in range(0, length):
    chain += current_word + " "
    current_word = retrieve_random_word(word_dict[current_word])

print(chain)
