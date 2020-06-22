# -*- coding: utf-8 -*-
# 

"""
用户认证登录
"""

import time
from core import db_handler


def login_check(func):
    def inner(*args, **kwargs):
        # 用户状态为真才能调用功能函数
        if args[0]['is_authenticated']:
            print('账号已登录')
            return func(*args, **kwargs)
        else:
            exit('Account not logged in ')
    return inner


def login(username, password):
    """
    登录
    :param username: 用户名
    :param password: 密码
    :return:
    """
    # 这里返回得到的是file_execute 函数的内存地址
    db_api = db_handler.db_handler()
    # 查询用户是否存在
    account_data = db_api('select * from accounts where account=%s' % username)
    if account_data['password'] == password:
        # 解析时间为时间戳
        expire_date_stamp = time.mktime(time.strptime(account_data['expire_date'], '%Y-%m-%d'))
        if time.time() > expire_date_stamp:
            # 账号过期时间大于当前时间就表示已经过期
            print('%s account has expired' % username)
        else:
            # 返回用户数据
            return account_data
    else:
        print('user password error')


def user_login(acc_data, log_obj):
    """
    用户登录
    :param acc_data: 初始数据
    :param log_obj: 日志对象
    :return:
    """
    retry = 0  # 重试次数
    while retry < 3 and acc_data['is_authenticated'] is not True:
        username = input("\033[31m input username: \033[0m")
        password = input("\033[31m input account password: \033[0m")
        data = login(username, password)
        if data:
            acc_data['account_id'] = username
            # 更改用户登录状态
            acc_data['is_authenticated'] = True
            # 返回用户数据
            return data
        # 登录失败,重试次数加1
        retry += 1
    else:
        log_obj.error("account [%s] too many login attempts" % username)
        exit()
