from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import re

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='65700',
                       db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE wikipedia")


def insert_page_if_not_exists(url):
    """查询url是否在pages表中存在 如果存在就返回id 不存在就插入后返回id"""
    cur.execute("SELECT * FROM pages WHERE url = %s", url)
    if cur.rowcount == 0:
        cur.execute("INSERT INTO pages (url) VALUES (%s)", url)
        conn.commit()
        return cur.lastrowid   # 返回最后一个插入的行的主键id
    else:
        return cur.fetchone()[0]  # 返回查询到的url的主键id


def insert_link(from_page_id, to_page_id):
    """如果链接不存在就插入"""
    cur.execute("SELECT * FROM links WHERE fromPageID = %s AND toPageId = "
                "%s", (int(from_page_id), int(to_page_id)))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO links (fromPageID, toPageId) VALUES (%s, "
                    "%s)", (int(from_page_id), int(to_page_id)))
        conn.commit()


pages = set()


def get_links(page_url, recursion_level):
    """深度优先搜索？式的获取页面url，当递归深度超过4，就中断操作"""
    global pages
    if recursion_level > 4:
        return
    page_id = insert_page_if_not_exists(page_url)
    html = urlopen("http://en.wikipedia.org" + page_url)
    bs_obj = BeautifulSoup(html, "lxml")
    for link in bs_obj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        insert_link(page_id, insert_page_if_not_exists(link.attrs['href']))
        if link.attrs['href'] not in pages:
            # 遇到一个新页面，加入集合并搜索里面的词条链接
            new_page = link.attrs['href']
            pages.add(new_page)
            get_links(new_page, recursion_level + 1)


get_links("/wiki/Kevin_Bacon", 0)
cur.close()
conn.close()