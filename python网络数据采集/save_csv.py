# # -*- coding:utf-8 -*-
# import csv
#
# csv_file = open("test.csv", "w+")
# try:
#     writer = csv.writer(csv_file)
#     writer.writerow(("数字", "数字加2", "数字乘2"))
#     for i in range(10):
#         writer.writerow((i, i + 2, i * 2))
# finally:
#     csv_file.close()


import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bsObj = BeautifulSoup(html, "lxml")
# 主对比表格是当前页面上的第一个表格
table = bsObj.findAll("table", {"class": "wikitable"})[0]
rows = table.findAll("tr")
csvFile = open("editors.csv", 'wt', newline="", encoding='utf-8')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)
finally:
    csvFile.close()
