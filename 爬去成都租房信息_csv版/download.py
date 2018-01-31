# -*- coding: utf-8 -*-
from random import sample
from datetime import datetime
from 爬去成都租房信息_csv版.c_ip import use_proxy, del_ip, get_ips
from 爬去成都租房信息_csv版.models import Throttle

import requests

user_agent_list = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
                   "Opera/8.0 (Windows NT 5.1; U; en)",
                   "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
                   "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
                   "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
                   "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
                   "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
                   "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
                   "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                   "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                   "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
                   "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
                   "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                   "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                   "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                   "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
                   "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
                   "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
                   "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
                   "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
                   "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
                   ]
# 随机选取一个用户代理
USER_AGENT = sample(user_agent_list, 1)[0]
# 默认等待时间
DEFAULT_DELAY = 5
# 默认重试次数
DEFAULT_RETRIES = 5
# 默认等待超时
DEFAULT_TIMEOUT = 10
# 请求头
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,'
              'application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': USER_AGENT
}


class DownLoad:
    """
    下载指定url的内容并返回其html
    :param headers: 头部信息
    :param proxy: bool值 True or False
    :param timeout: 请求超时时间
    :param delay:  下载间隔时间
    :param cache:   储存方法 如：CsvCache()
    :param retries: 重试次数
    :return dict : {'html': html, 'code': code}
    """
    def __init__(self, headers=HEADERS, proxy=False,
                 timeout=DEFAULT_TIMEOUT, delay=DEFAULT_DELAY,
                 cache=None, retries=DEFAULT_RETRIES):
        self.throttle = Throttle(delay)
        self.use_proxy = proxy
        if self.use_proxy:
            # 获取ip代理池
            self.proxies = get_ips()
        self.proxy = {}
        self.timeout = timeout
        self.headers = headers
        self.cache = cache
        self.num_retries = retries

    def __call__(self, url):
        result = None
        print('-----------------开始下载:{url}----------------------'.format(
            url=url))
        if self.cache:
            # 如果有存储方式
            try:
                # 查看缓存中是否已经下载
                result = self.cache[url]
            except:
                # 没有
                pass
            else:
                # 已经下载了，查看响应码
                if self.num_retries > 0 and (result['code'] is None or 500 <= \
                        result['code'] < 600):
                    # 服务器错误，因此忽略缓存和重新下载的结果
                    print('被反爬？')
                    result = None
                else:
                    if result['code'] is None and result['html'] == '':
                        result = None
                    else:
                        pass
                        # print('已有缓存!{}'.format(url))
        if result is None:
            self.throttle.wait(url)
            result = self.download(url)
            if self.cache and result['code']:
                self.cache[url] = result
        return result['html']

    # @use_proxy
    def download(self, url):
        """下载页面"""
        if self.use_proxy:
            # 随机选取一个代理ip
            self.proxy = {'http': sample(self.proxies, 1)[0]}
            print("使用代理:{}".format(self.proxy['http']))
        session = requests.Session()
        try:
            res = session.get(url, proxies=self.proxy,
                              headers=self.headers, timeout=self.timeout)
            # res = str(res.content, 'gbk')
            html = res.text
            code = res.status_code
        except requests.exceptions.ProxyError:
            print('代理异常：自动更换中...')
            del_ip(self.proxy)
            if self.num_retries > 0:
                self.num_retries -= 1
                self.proxy = {'http': sample(self.proxies, 1)[0]}
                print('代理更换为：{}'.format(self.proxy))
                print('尝试重新下载...')
                return self.download(url)
            else:
                print('重试次数已到达！请手动更换代理或者重试！')
                html = ''
                code = None
        except Exception as e:
            print("下载中出现错误", type(e))
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if self.num_retries > 0 and 500 <= code < 600:
                    self.num_retries -= 1
                    return self.download(url)
            else:
                code = None
        return {'html': html, 'code': code}

