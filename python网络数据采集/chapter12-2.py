# -*- coding: utf-8 -*-
"""
    处理cookie 新式生成cookie的方式可能需要点击按钮才会生成
所以，需要使用selenium+PhantomJS点击按钮后，再使用requests进行
cookie的设置
"""
from selenium import webdriver
driver = webdriver.PhantomJS(
    executable_path=r"D:\Web\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver.get("http://111.231.65.159/auth/login")
driver.implicitly_wait(1)
driver.find_element_by_name('username').send_keys('管理员')
driver.find_element_by_name('password').send_keys('admin')
driver.implicitly_wait(1)
driver.find_element_by_id('submit').click()
driver.implicitly_wait(3)
print(driver.get_cookies())

# 储存cookie以便其他爬虫使用
savedCookies = driver.get_cookies()

driver2 = webdriver.PhantomJS(
    executable_path=r"D:\Web\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver2.get("http://111.231.65.159")
print(driver2.get_cookies())
driver2.delete_all_cookies()
for cookie in savedCookies:
    driver2.add_cookie(cookie)

driver2.get("http://111.231.65.159")
driver.implicitly_wait(1)
print(driver2.get_cookies())

