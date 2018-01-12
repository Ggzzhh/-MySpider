# -*- coding: utf-8 -*-
"""使用selenium测试网站js内容"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# 动作链可以一次性释放多个操作
from selenium.webdriver import ActionChains


driver = webdriver.PhantomJS(
    executable_path=r"D:\Web\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver.get("http://pythonscraping.com/pages/files/form.html")

firstnameField = driver.find_element_by_name("firstname")
lastnameField = driver.find_element_by_name("lastname")
submitButton = driver.find_element_by_id("submit")

actions = ActionChains(driver).click(firstnameField).send_keys("Rr")\
    .click(lastnameField).send_keys("mitchell")\
    .send_keys(Keys.RETURN)  # 敲回车...
actions.perform()  # 这行代码运行时 执行actions中的操作

print(driver.find_element_by_tag_name("body").text)

driver.close()