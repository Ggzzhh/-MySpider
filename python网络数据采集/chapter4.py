from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
import json

random.seed(datetime.datetime.now())


def get_country(ip_address):
    """通过ip地址查找国家所在地"""
    try:
        response = urlopen("http://freegeoip.net/json/" + ip_address).read()\
            .decode("utf-8")
    except Exception as e:
        return e
    response_json = json.loads(response)
    return response_json.get('country_code')


def get_links(article_url):
    html = urlopen("http://en.wikipedia.org" + article_url)
    bs_obj = BeautifulSoup(html, "lxml")

    return bs_obj.find("div", {"id": "content"}).findAll(
        "a", href=re.compile("^(/wiki/)((?!:).)*$"))


def get_history_ips(page_url):
    """获取编辑历史页面的编辑人的ips"""
    # 编辑历史页面的URL链接的格式是：
    # http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    page_url = page_url.replace("/wiki/", "")  # 把 /wiki/ 替换为空
    history_url = "http://en.wikipedia.org/w/index.php?title=" \
                  + page_url + "&action=history"
    print("编辑历史页面的URL是：" + history_url)
    try:
        html = urlopen(history_url)
    except Exception as e:
        return e
    bs_obj = BeautifulSoup(html, "lxml")
    # 找出class = mw-anonuserLink的链接
    # 它们用ip地址代替用户名
    # ip = bs_obj.findAll("a", text=re.compile("([0-9]{2,3}\.){2}[0-9]{2,3}"))
    ip_addresses = bs_obj.findAll("a", {"class": "mw-anonuserlink"})
    address_list = set()
    for ip_address in ip_addresses:
        text = ip_address.get_text()
        address_list.add(text)
    return address_list


links = get_links("/wiki/Python_(programming_language)")

while len(links) > 0:
    for link in links:
        print("---------------------------------")
        history_ips = get_history_ips(link.attrs['href'])
        for history_ip in history_ips:
            country = get_country(history_ip)
            if country is not None:
                print(history_ip + "来自：" + country)

    new_link = links[random.randint(0, len(links-1))].attrs['href']
    links = get_links(new_link)
