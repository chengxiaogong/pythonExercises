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
    # 创建一个handler,用于写入到日志文件
    file_handler = logging.FileHandler(r'..\\logs\\bank.log',encoding='utf-8')
    # 创建一个handler,用于输出到控制台
    ch_handler = logging.StreamHandler()
    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s %(name)s %(message)s', datefmt='%Y%m%d %H:%M:%S')
    # 设置输出到日志文件中的格式
    file_handler.setFormatter(formatter)
    # 设置输出到控制台中的格式
    ch_handler.setFormatter(formatter)
    # logger 添加文件handler对象和控制台handler 对象
    logger.addHandler(file_handler)
    logger.addHandler(ch_handler)

    return logger


if __name__ == '__main__':
    logger().info("hello world")
