#概述
* 仿照Scrapy-redis开发的基于redis开发的简易分布式爬虫框架，将redis作为队列使用，
提取url，然后下载并将结果传入某解析函数即可, 爬虫经验较少，比较简单。
* 项目不大，文档也写不好，自学的人伤不起！╮(╯▽╰)╭
* 求指点，求基友，有意者请联络471992509@qq.com！╮(╯▽╰)╭
* 想转行自学了python，找工作ing，联系方式↑ ╮(╯▽╰)╭

#详细

### 开发环境
* Python 3.6
* Requests 
* Redis 3.2.100
* Pycharm(非必需，但可能出现bug)

### 运行环境
Win 10 + Redis 3.2.100(已测试)
Mac (待测试)

### 实现功能
分布式爬虫，可并发

### 需求分析
作为一个分布式爬虫框架，方便的部署到多个环境上，快速的获取数据，简易的使用，
在运行中忽略某些错误，以及在遇到某些情况时停止抓取，管理者强制停止爬虫时可以
将正在进行的线程进行完等，个人理解中大体需求如此。

### 程序实现
* 目前程序算是基础版本(0.1？赫赫)，实现了如下功能：
    1. 分布式： 只需要一台redis服务器，其余爬虫链接到服务器获取url进行数据采集即可。
    2. 部署方便： 文件夹copy一下就行，python本身就可以跨平台进行运转。
    3. 快速获取数据： 下载使用的是requests库，快慢完全凭借自己，调整settings.py中的delay以及max_threads就行。
    4. 使用简单： 继承一下爬虫类，写个解析函数，跟scrapy类似，简化版。
    5. 错误处理： 目前除了ctrl+C和关闭窗口以外，只有level_time到了才能停止程序。
    6. 停止处理： ctrl+c后会完成线程后再停止。
    7. 统计： 目前只统计进行了多少次抓取，没有计算成功与失败次数。
    8. 日志： 部分情况会纪录日志，不过比较少，不过可以自己定制。 
    9. 代理:  代理和headers当然可设置。
* 代码结构：
    * \_\_init__.py   初始化文件，实例化日志
    * download.py     下载器类
    * scheduler.py    调度器类（虽然功能不全）
    * settings.py     默认设置
    * spider.py       爬虫类  
    * logs.log        日志文件
    * example.py      示例
    * README.md       说明
* 部分源码展示：
```python
# download.py
class DOWNLOAD:

    def __init__(self, proxy=None, delay=DELAY, num_retries=NUM_RETRIES,
                 timeout=TIMEOUT, headers=HEADERS, **kwargs):
        """
        初始化
        :param proxy: 下载时使用的代理
        :param delay:  下载延迟
        :param timeout: 下载超时时间
        :param headers: 下载时使用的文件头
        :param num_retries: 下载重试次数
        :param kwargs:  其他
        """
        self.proxy = proxy
        self.timeout = timeout
        self.headers = headers or {'User-agent': 'OSpider'}
        self.logging = logger
        self.throttle = Throttle(delay)
        self.num_retries = num_retries
        self.kwargs = kwargs
    
    def __call__(self, url, method='GET', data=None, cookies=None, **kwargs):
        """
        这个魔法函数可以让类的实例像函数一样被调用，例如：
        D = DOWNLOAD(...)
        result = D(url)
        :param url:  url
        :param method:  请求的方法
        :param data:    请求的内容
        :param cookies: 请求时使用的cookies
        :param kwargs:  其他，比如代理
        :return: {'html': 网页内容, 'status': 状态码, 'url': 请求地址}
        """
        # 设置同个域下的限速
        self.throttle.wait(url)
        # 让类的实例返回download函数的返回值
        return self.download(url, method, data, cookies)
    
    def download(self, url, method='GET', data=None, cookies=None):
        """
        具体下载用函数
        :param url: 请求地址
        :param method: 请求方法
        :param data: 请求附带的内容
        :return: {'html': 网页内容, 'status': 状态码, 'url': 请求地址}
        """
        methods = ["GET", "POST", "PUT", "DELETE"]
        session = requests.Session()
        # 设置头信息
        session.headers = self.headers
        # 设置代理
        if self.proxy:
            if isinstance(self.proxy, dict):
                if self.proxy.get('http') or self.proxy.get('https'):
                    session.proxies = self.proxy
                    self.logging.info('设置代理:{}'.format(self.proxy))
            else:
                self.logging.error('代理格式错误，需要使用字典格式')
        # 检查请求方法
        if method not in methods:
            raise ValueError("请求方法错误, 请在{}中选择!".format(methods))
        # 设置cookies
        if cookies:
            session.cookies = cookies
        # 获取内容并返回
        try:
            res = session.request(method, url, data=data)
            html = res.text
            status = res.status_code
        # 出现问题打印到日志，然后重试num_retries次
        except Exception as e:
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if self.num_retries > 0 and 500 <= code < 600:
                    self.num_retries -= 1
                    return self.download(url, method, data, cookies)
            else:
                code = None
            self.logging.error(e)
            html = None
            status = None
        return {'html': html, 'status': status, 'url': url}

# Scheduler.py
"""
    SCHEDULER（调度器） 目前只有抓取然后返回结果的功能.....
"""
# 初始化就略过了，选了两个较重要的放了上来
# 使用threading达成了并发抓取，因为是密集型IO所以影响不大。
def run(self):
    """开始进行抓取"""
    threads = []
    wait = 0
    try:
        while True:
            num = self.show_num()
            if num is None or num == 0:
                print('抓捕队列为空！{}秒后继续抓取'.format(self.wait_time))
                time.sleep(self.wait_time)
                wait += self.wait_time
                if wait >= self.leave_time:
                    print('{}秒内获取不到url，程序终端'.format(self.leave_time))
                    break
                continue
            for thread in threads:
                if not thread.is_alive():
                    # 移除停止活动的线程
                    threads.remove(thread)
            # 如果活动的线程数没有到达最大线程就继续创建线程
            while len(threads) < self.max_threads:
                thread = threading.Thread(target=self.crawl)
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)
            time.sleep(3)
    # 按了CTRL+c之后....
    except KeyboardInterrupt:
        self.leave_time = 0
        # 等待线程结束然后移除还在活动的线程
        for thread in threads:
            thread.join()
            if thread.is_alive():
                threads.remove(thread)
        print('程序停止!')
        print('花费时间{}'.format(datetime.now() - self.start_time))
        print('采集了{}个url'.format(self.start_num - self.show_num()))
        
def crawl(self):
    """抓取流程控制函数"""
    while True:
        # 设置一个可以在外部控制循环结束的条件
        if self.leave_time == 0:
            break
        url = self.get_url()
        if url is None:
            break
        res = self.D(url, **self.kwargs)
        if self.callback:
            self.callback(response=res)
        else:
            pprint('没有解析函数，直接打印结果：')
            pprint(res)
```

### 程序使用方法以及截图
```python
# 例子
# example.py
import json
import redis
from OSpider import OSPIDER, logger

# 继承爬虫类，其实这个类也没啥东西, 就是调用了一下调度器类，所以不展示了。
class T(OSPIDER):
    # 创建一个存储用的redis链接
    r = redis.StrictRedis()
    # 爬虫类中也有一个解析函数，这个函数有一个要求，有个参数必须名为response

    def parse(self, response):
        # 例子中采集的url是知乎的api，返回一个json数据，所以比较简单。
        # 这里也就是获取了一下url_token，其实是无意义行为，举例用。
        try:
            res = json.loads(response['html'])
            self.r.lpush('zhihu.url_token', res['url_token'])
            print(res['name'])
        except Exception:
            # 导入的logger用的是自带的logging模块，日志同时会打印到屏幕以及日志文件中去。
            logger.info("{}--出现错误，状态码--{}"
                        .format(response['url'], response['status']))


if __name__ == '__main__':
    # 运行....
    t = T()
    t.run()
```