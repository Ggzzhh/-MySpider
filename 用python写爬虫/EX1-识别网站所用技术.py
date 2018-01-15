# -*- coding: utf-8 -*-
"""查询构建网站所使用的技术  builtwith"""
import builtwith

parse = builtwith.parse('http://example.webscraping.com')
print(parse)