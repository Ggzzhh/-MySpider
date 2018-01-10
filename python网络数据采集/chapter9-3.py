# -*- coding: utf-8 -*-
"""处理HTTP认证"""
import requests
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('Test', 'password')
r = requests.post(url="http://pythonscraping.com/pages/auth/login.php",
                  auth=auth)
print(r.text)
