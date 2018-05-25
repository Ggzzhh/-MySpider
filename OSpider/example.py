# -*- coding: utf-8 -*-
try:
    import OSpider
except:
    import sys
    import os
    sys.path.append(os.path.abspath('..'))
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

