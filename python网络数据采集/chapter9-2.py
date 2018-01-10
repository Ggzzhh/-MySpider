# -*- coding: utf-8 -*-
"""使用requests库中的Session来跟踪会话"""
import requests

session = requests.Session()

params = {'username': 'username', 'password': 'password'}
s = session.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
print("cookie is set to: ")
print(s.cookies.get_dict())
print('------------')
print("前往资料页面")
s = session.get("http://pythonscraping.com/pages/cookies/profile.php")
print(s.text)