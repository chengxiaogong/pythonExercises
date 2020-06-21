# -*- coding: utf-8 -*-
# 


"""
日志记录模块
"""

import os
import logging
from conf import settings


def log_func(log_type):
    """
    日志处理
    :param log_type: 日志类型
    :return:
    """
    logger = logging.getLogger(log_type)
    # 设置日志的级别
    logger.setLevel(settings.LOGS_LEVEL)
    # 创建handler , 用于输出到控制台
    ch = logging.StreamHandler()
    # 定义日志的输出路径
    file_path = os.path.join(settings.BASE_DIR, 'log', settings.LOG_TYPES[log_type])
    # 创建handler , 用于输出到文件中
    fh = logging.FileHandler(file_path)
    # 定义日志的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # 设置输出到屏幕上的日志格式
    ch.setFormatter(formatter)
    # 设置输出到文件中的日志格式
    fh.setFormatter(formatter)
    # logger 对象添加多个fh/ch 对象
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
