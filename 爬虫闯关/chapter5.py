# -*- coding: utf-8 -*-
from PIL import Image, ImageOps
import requests
import pytesseract
from 爬虫闯关.chapter2 import parse_html
from 爬虫闯关.chapter3 import login

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver

USERNAME = '123312'
PASSWORD = '123123'
login_url = 'http://www.heibanke.com/accounts/login'
seed_url = "http://www.heibanke.com/lesson/crawler_ex04/"


# 进行验证码去噪以及辨认
def image_to_str():
    # 读取图片
    image = Image.open("valiCode.jpg")
    # 转换图像格式为RGBA
    image = image.convert("RGBA")
    # 读取图像
    pixdata = image.load()
    # 把红色<90的像素变为白色
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)
    # 把绿色<136的像素变为白色
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)
    # 把蓝色>0的像素变为黑色
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)

    image.resize((1000, 500), Image.NEAREST)
    image.save('valiCode.gif', 'GIF')
    return pytesseract.image_to_string(Image.open('valiCode.gif'))


def cleanImage(imagePath):
    """清理并保存验证图片"""
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x < 143 else 255)
    borderImage = ImageOps.expand(image, border=20, fill='white')
    borderImage.save(imagePath)


def get_captcha(html):
    soup = BeautifulSoup(html, 'lxml')
    e = soup.find('img')
    img_url = urlparse(seed_url).scheme + "://" + urlparse(
        seed_url).netloc + e.get('src')
    img = requests.get(img_url)
    with open('valiCode.jpg', 'wb') as f:
        f.write(img.content)
    # cleanImage('valiCode.jpg')
    return image_to_str()

print('开始测试')
# driver = webdriver.PhantomJS(
#     executable_path=r"D:\Web\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver = webdriver.Firefox()
driver.get(login_url)
driver.find_element_by_id('id_username').send_keys(USERNAME)
driver.find_element_by_id('id_password').send_keys(PASSWORD)
driver.find_element_by_id('id_submit').click()
if driver.current_url != login_url:
                print("登录成功！")
driver.get(seed_url)

i = 4
while i != 30:
    driver.find_element_by_id('id_username').send_keys('test')
    driver.find_element_by_id('id_password').send_keys(i)
    vali_code = driver.find_element_by_tag_name('img')
    vali_code.screenshot('valiCode.jpg')
    code = image_to_str()
    driver.find_element_by_id('id_captcha_1').send_keys(code)
    driver.find_element_by_id('id_submit').click()
    if driver.find_element_by_tag_name('h3').text == '验证码输入错误':
        print('验证码错误', code)
        continue
    if driver.find_element_by_tag_name('h3').text == '您输入的密码错误, 请重新输入':
        print('密码错误', i)
        i += 1
        continue
    print("密码", i)



