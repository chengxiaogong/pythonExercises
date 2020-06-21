# -*- coding: utf-8 -*-
# 

"""
配置模块
"""

import os
import logging


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

# 日志级别
LOGS_LEVEL = logging.INFO
# 日志文件名
LOG_TYPES = {
    'transaction': 'transaction.log',
    'access': 'access.log'
}

# 数据库 配置
DATABASE = {
    'engine': 'file_storage',  # support mysql, postgresql in the future
    'name': 'accounts',
    'path': "%s/db" % BASE_DIR
}

# 交易类型
TRANSACTION_TYPE = {
    'repay': {'action': 'plus', 'interest': 0},
    'withdraw': {'action': 'minus', 'interest': 0.05},
    'transfer': {'action': 'minus', 'interest': 0.05},
    'consume': {'action': 'minus', 'interest': 0},
}
