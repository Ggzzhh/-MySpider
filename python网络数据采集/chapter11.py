# -*- coding: utf-8 -*-
"""获取验证码提交答案  pytesseract 识别的不是很好"""

import pytesseract
import requests
from urllib.request import urlretrieve
from urllib.request import urlopen
from PIL import Image, ImageOps
from bs4 import BeautifulSoup


def cleanImage(imagePath):
    """清理并保存验证图片"""
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x < 143 else 255)
    borderImage = ImageOps.expand(image, border=20, fill='white')
    borderImage.save(imagePath)


html = urlopen("http://www.pythonscraping.com/humans-only")
bsObj = BeautifulSoup(html, "html5lib")
# 收集需要处理的表单数据
imageLocation = bsObj.find("img", {'title': 'Image CAPTCHA'})["src"]
formBuildId = bsObj.find("input", {'name': 'form_build_id'})["value"]
captchaSid = bsObj.find("input", {'name': 'captcha_sid'})["value"]
captchaToken = bsObj.find("input", {'name': 'captcha_token'})["value"]

captchaUrl = "http://pythonscraping.com"+imageLocation
urlretrieve(captchaUrl, 'captcha.jpg')
cleanImage('captcha.jpg')
captchaResponse = pytesseract.image_to_string(Image.open('captcha.jpg'))
captchaResponse = captchaResponse.replace(" ", "").replace("\n", "")
print("captchaResponse: " + captchaResponse)
