# -*- coding: utf-8 -*-

import OSpider.settings
import logging
# logging.basicConfig(level=settings.LEVEL,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %('
#                            'message)s')

logger = logging.getLogger('OSpider')
logger.setLevel(level=settings.LEVEL)
handler = logging.FileHandler("logs.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)

from OSpider.spider import OSPIDER
