from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import pymysql

conn = pymysql.connect(host="127.0.0.1", user='root', passwd='65700',
                       db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE scraping")


def store(title, content):
    """把数据存储到数据库中"""
    cur.execute("INSERT INTO pages (title, content) VALUES (\"%s\", \"%s\")",
                (title, content))
    cur.connection.commit()


def get_links(article_url):
    html = urlopen("http://en.wikipedia.org" + article_url)
    bs_obj = BeautifulSoup(html, "lxml")
    title = bs_obj.find("h1").get_text()
    content = bs_obj.find("div", {"id": "mw-content-text"}).find("p").get_text()
    store(title, content)
    return bs_obj.find("div", {"id": "content"}).findAll(
        "a", href=re.compile("^(/wiki/)((?!:).)*$"))


links = get_links("/wiki/Kevin_Bacon")
try:
    while len(links) > 0:
        new_article = links[random.randint(0, len(links) - 1)].attrs["href"]
        print(new_article)
        links = get_links(new_article)
finally:
    cur.close()
    conn.close()