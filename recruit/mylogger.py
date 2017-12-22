# -*- coding:utf-8 -*-

import logging
from logging import FileHandler, Formatter

logger = logging.getLogger('custom.logger')

#file_name = "/home/sumin/study/recruit/logs/recruit.log"
file_name = "./recruit.log"
log_file_handler = FileHandler(filename=file_name, mode='a', encoding='utf-8')
log_formatter = Formatter("[%(process)d:%(processName)s:%(thread)d:%(threadName)s] %(asctime)s : %(message)s [in %(pathname)s:%(lineno)d]")
log_file_handler.setFormatter(log_formatter)
logger.setLevel(logging.INFO)
logger.addHandler(log_file_handler)

