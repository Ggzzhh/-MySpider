# -*- coding: utf-8 -*-
"""简单的设置cookie 通过验证"""
import requests

params = {'username': 'Test', 'password': 'password'}
r = requests.post("http://pythonscraping.com/pages/cookies/welcome.php", params)

print("cookie 设置值在：")
print(r.cookies.get_dict())
print("----------")
print("前往资料页面")
r = requests.get("http://pythonscraping.com/pages/cookies/profile.php",
                 cookies=r.cookies)
print(r.text)
