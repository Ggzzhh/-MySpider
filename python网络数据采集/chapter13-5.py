# -*- coding: utf-8 -*-
"""
selenium 鼠标拖放动作
selenium 截屏操作 driver.get_screenshot_as_file('tmp/p.png')
"""

from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.PhantomJS(
    executable_path=r"D:\Web\phantomjs-2.1.1-windows\bin\phantomjs.exe")
# driver.get('http://pythonscraping.com/pages/javascript/draggableDemo.html')
#
# print(driver.find_element_by_id("message").text)
#
# element = driver.find_element_by_id("draggable")
# target = driver.find_element_by_id("div2")
# actions = ActionChains(driver)
# actions.drag_and_drop(element, target).perform()
#
# print(driver.find_element_by_id("message").text)

driver.get('http://www.pythonscraping.com/')
driver.get_screenshot_as_file('pythonscraping.png')