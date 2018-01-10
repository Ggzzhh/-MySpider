# -*- coding: utf-8 -*-
"""
        处理重定向 方法：页面开始加载时“监视”DOM中的一个，
    然后重复调用直到这个元素消失，就说明网站已经跳转!
        这个程序每半分钟检查一次网页，看看 html 标签还在
    不在，时限为 10 秒钟，不过检查的时间间隔和时限都可以
    根据实际情况随意调整。
"""

from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException


def wait_for_load(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while 1:
        count += 1
        if count > 20:
            print("时间超过10秒，return")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return

driver = webdriver.PhantomJS(
    executable_path=r"D:\Web\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver.get("http://pythonscraping.com/pages/javascript/redirectDemo1.html")
wait_for_load(driver)
print(driver.page_source)