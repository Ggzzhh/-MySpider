# -*- coding: utf-8 -*-
"""更好的动态采集方法 让selenium不断的检查某个元素是否存在,以此确定是否已经完全加载"""
from selenium import webdriver
# driver.find_element(By.ID, "content") 等于 driver.find_element_by_id("content")
from selenium.webdriver.common.by import By
# 隐式等待
from selenium.webdriver.support.ui import WebDriverWait
# 期望等待条件
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS(
    executable_path=r"D:\Web\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
try:
    # 隐式等待直到id为loadedButton的按钮出现或者到达10秒
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(By.ID, "loadedButton")
    )
finally:
    print(driver.find_element_by_id("content").text)
    driver.close()