# -*- coding: utf-8 -*-
import requests
import base64
import re
import rsa
import time
import json
import binascii
from bs4 import BeautifulSoup


class UserLogin:
    """微博模拟登陆"""

    def __init__(self, username="", pwd=""):
        """构造函数 constructor"""
        self.username = username
        self.password = pwd
        self.data = {}

        self.session = requests.Session()
        self.session.headers.update(
            {
                'User-Agent': "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50"
            }
        )
        self.session.get("https://login.sina.com.cn/signup/signin.php")
        self.prelogin_url = "https://login.sina.com.cn/sso/prelogin.php"
        self.login_url = "https://login.sina.com.cn/sso/login.php?client" \
                         "=ssologin.js(v1.4.19)&_={}"

    def login(self):
        """
        登陆 登陆成功返回session 失败raise一个ValueError
        """
        self.get_json_data()
        post_data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": self.get_username(),
            "service": "miniblog",
            "servertime": self.data['servertime'],
            "nonce": self.data['nonce'],
            "pwencode": "rsa2",
            "rsakv": self.data['rsakv'],
            "sp": self.get_pwd(),
            "sr": "1280*800",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "40",
            "returntype": "TEXT"
        }
        resp = self.session.post(self.login_url.format(str(int(time.time()))),
                                 data=post_data).json()
        if resp['retcode'] == '0':
            params = {
                "callback": "sinaSSOController.callbackLoginStatus",
                "client": "ssologin.js(v1.4.19)",
                "ticket": resp["ticket"],
                "ssosavestate": int(time.time()),
                "_": int(time.time() * 1000),
            }
            url = "https://passport.weibo.com/wbsso/login"
            response = self.session.get(url, params=params)
            data = re.findall(r'(?<=\().*(?=\))', response.text)
            data = json.loads(data[0])
            if data['result']:
                return self.session
            else:
                raise ValueError

    def get_json_data(self):
        """获取公共数据"""
        params = {
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "su": self.get_username(),
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1=.4.15)",
            "_": int(time.time() * 1000)
        }
        resp = self.session.get(self.prelogin_url, params=params)
        # print(resp.text)
        data = re.findall(r'(?<=\().*(?=\))', resp.text)
        self.data = json.loads(data[0])

    def get_username(self):
        """通过base64的方式加密用户名"""
        return base64.b64encode(
            self.username.encode(encoding='utf-8')
        ).decode("utf-8")

    def get_pwd(self):
        """通过类似新浪的加密方式获取加密后的密码"""
        rasKey = int(self.data['pubkey'], 16)
        # 创建一个rsa的公匙
        key = rsa.PublicKey(rasKey, int("10001", 16))
        # 信息整合成一个字符串
        msg = str(self.data['servertime']) + "\t" + str(self.data['nonce']) +\
              "\n" + str(self.password)
        # 使用公匙进行加密
        pwd = rsa.encrypt(msg.encode(encoding='utf-8'), key)
        # 转换为2进制的16进制表示并返回
        return binascii.hexlify(pwd)


if __name__ == "__main__":
    login = UserLogin("y471992509", "Gg65700")
    # print(login.get_username() == "eTQ3MTk5MjUwOQ==")
    # login.get_json_data()
    session = login.login()
    session.get("http://s.weibo.com/weibo/%25E9%2583%2591%25E5%25B7%259E"
                 "%25E8%25BD%25BB%25E5%25B7%25A5%25E4%25B8%259A%25E5%25A4%25A7%25E5%25AD%25A6&Refer=index")
    print(session.cookies)