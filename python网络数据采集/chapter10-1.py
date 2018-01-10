# -*- coding: utf-8 -*-
"""使用selenium以及phantomjs来采集JavaScript"""
from selenium import webdriver
import time

driver = webdriver.PhantomJS(
    executable_path=r"D:\Web\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
time.sleep(3)
print(driver.find_element_by_id('content').text)
driver.close()