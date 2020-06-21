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
        print('验证账号有没有登录')
        if args[0]['is_authenticated']:
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
    db_api = db_handler.db_handler()
    # 查询用户是否存在
    account_data = db_api('select * from accounts where account=%s' % username)
    if account_data['password'] == password:
        # 解析时间为时间戳
        expire_date_stamp = time.mktime(time.strptime(account_data['expire_date'], '%Y-%m-%d'))
        if time.time() > expire_date_stamp:
            print('%s account has expired' % username)
        else:
            return account_data
    else:
        print('user password error')


def user_login(acc_data, log_obj):
    retry = 0
    while retry < 3 and acc_data['is_authenticated'] is not True:
        username = input("\033[31m input username: \033[0m")
        password = input("\033[31m input account password: \033[0m")
        data = login(username, password)
        if data:
            acc_data['account_id'] = username
            acc_data['is_authenticated'] = True
            return data
        retry += 1
    else:
        log_obj.error("account [%s] too many login attempts" % username)
        exit()
