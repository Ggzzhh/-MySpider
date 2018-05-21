# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup

# driver = webdriver.PhantomJS(
#     executable_path=r"D:\Web\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver = webdriver.Chrome()
driver.get('http://music.163.com/playlist?id=446989006')
content = driver.page_source.encode('utf-8')
# driver.find_element_by_id('search_term').send_keys('.')
# driver.execute_script(
#     "document.getElementById('page_size').options[1].text = '1000'")
# driver.find_element_by_id('search').click()
# driver.implicitly_wait(30)
# links = driver.find_elements_by_css_selector('#results a')
# countries = [link.text for link in links]
driver.close()
print(BeautifulSoup(content, 'lxml').find('ul', {"class": "f-hide"}))