from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

download_directory = "downloaded"
base_url = "http://pythonscraping.com"


def get_absolute_url(base_url, source):
    """获取绝对的url"""
    if source.startswitch("http://www."):
        url = "http://" + source[11:]
    elif source.startswitch("http://"):
        url = source
    elif source.startswitch("www."):
        url = "http://" + source[4:]
    else:
        url = base_url + "/" + source

    if base_url not in url:
        return None
    return url


def get_download_path(base_url, absolute_url, download_directory):
    """获取下载路径"""
    path = absolute_url.replace("www", "")
    path = path.replace(base_url, "")
    path = download_directory + path
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    return path


html = urlopen("http://www.pythonscraping.com")
bsObj = BeautifulSoup(html, "lxml")
image_location = bsObj.find("a", {"id": "logo"}).find("img")["src"]
urlretrieve(image_location, "logo.jpg")
