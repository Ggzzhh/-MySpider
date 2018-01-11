# -*- coding: utf-8 -*-

"""如何避免踩入不可见的蜜罐"""
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.PhantomJS(
    executable_path=r"D:\Web\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver.get("http://pythonscraping.com/pages/itsatrap.html")
links = driver.find_elements_by_tag_name("a")
for link in links:
    if not link.is_displayed():
        print("这个链接" + link.get_attribute("href") + "是一个蜜罐")

fields = driver.find_elements_by_tag_name("input")
for field in fields:
    if not field.is_displayed():
        print("不要更改这个标签的值:" + field.get_attribute('name'))