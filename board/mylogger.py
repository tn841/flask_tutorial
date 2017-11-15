# -*- coding:utf-8 -*-

import logging
from logging import FileHandler, Formatter

logger = logging.getLogger('custom.logger')

from datetime import datetime
log_date = datetime.now().strftime('%Y-%m-%d')

log_file_handler = FileHandler(filename="/home/sumin/log/board/"+log_date+".log", mode='a', encoding='utf-8')
log_formatter = Formatter("[%(process)d:%(processName)s:%(thread)d:%(threadName)s] %(asctime)s : %(message)s [in %(pathname)s:%(lineno)d]")
log_file_handler.setFormatter(log_formatter)
logger.setLevel(logging.INFO)
logger.addHandler(log_file_handler)