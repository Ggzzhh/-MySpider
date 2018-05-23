# -*- coding: utf-8 -*-
# import .settings

import logging
# logging.basicConfig(level=settings.LEVEL,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %('
#                            'message)s')

logger = logging.getLogger('OSpider')

fh = logging.FileHandler('logs.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s][%(thread)d][%(filename)s][line: '
                              '%(lineno)d][%(levelname)s] :: %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)
