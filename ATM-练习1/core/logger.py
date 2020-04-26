# _*_ coding; utf-8 _*_
# author: cc
#

import logging

"""
需求:
用户转账、登录、提现操作均记录日志,日志文件位置如下
20190502 18:34:23  alex   transfer      transfered to  [tesla_company]  with amount RMB950000, intrest is RMB47500.
"""

def logger():
    logger = logging.Logger('alex', level=logging.DEBUG)
    file_handler = logging.FileHandler(r'..\\logs\\bank.log',encoding='utf-8')
    ch_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)s %(message)s', datefmt='%Y%m%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    ch_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(ch_handler)

    return logger


if __name__ == '__main__':
    logger().info("hello world")
