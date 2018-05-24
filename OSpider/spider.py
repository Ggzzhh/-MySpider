# -*- coding: utf-8 -*-
try:
    import OSpider
except:
    import sys
    import os
    sys.path.append(os.path.abspath('..'))

from OSpider import logger
from OSpider.Scheduler import SCHEDULER


class OSPIDER:
    def __init__(self):
        pass

    def parse(self, response):
        pass

    def run(self, proxy=None, method="GET", data=None):
        scheduler = SCHEDULER(callback=self.parse, proxy=proxy,
                              method=method, data=data)
        scheduler.run()