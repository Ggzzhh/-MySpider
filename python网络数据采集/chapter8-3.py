# -*- coding: utf-8 -*-
"""自然语言工具包的使用"""
# from nltk import word_tokenize
# from nltk import Text
#
# tokens = word_tokenize("Here is some not very interesting text")
# text = Text(tokens)
#
# print(text)

from nltk.book import *
from nltk import ngrams

fourgrams = ngrams(text6, 4)
for fourgram in fourgrams:
    if fourgram[0] == "coconut":
        print(fourgram)
