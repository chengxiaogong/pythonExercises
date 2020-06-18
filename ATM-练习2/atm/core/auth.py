#!_*_coding:utf-8_*_
#__author__:"Alex Li"
import os
from core import db_handler
from conf import settings
from core import logger
import json
import time


def login_required(func):
    # 验证用户是否登录
    def wrapper(*args, **kwargs):
        # 用户登录状态为真才能调用功能方法
        if args[0].get('is_authenticated'):
            return func(*args, **kwargs)
        else:
            exit("User is not authenticated.")
    return wrapper


def acc_auth(account, password):
    '''
    account auth func
    :param account: credit account number
    :param password: credit card password
    :return: if passed the authentication , retun the account object, otherwise ,return None
    '''
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account)
    print(account_file)
    if os.path.isfile(account_file):
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            if account_data['password'] == password:
                exp_time_stamp = time.mktime(time.strptime(account_data['expire_date'], "%Y-%m-%d"))
                if time.time() > exp_time_stamp:
                    print("\033[31;1mAccount [%s] has expired,please contact the back to get a new card!\033[0m"
                          % account)
                else:  # passed the authentication
                    return account_data
            else:
                print("\033[31;1mAccount ID or password is incorrect!\033[0m")
    else:
        print("\033[31;1mAccount [%s] does not exist!\033[0m" % account)


def acc_auth2(account, password):
    """
    优化版认证接口
    :param account: credit account number
    :param password: credit card password
    :return: if passed the authentication , retun the account object, otherwise ,return None
    """
    db_api = db_handler.db_handler()  # 这里得到的是文件执行方法的内存地址
    # 查询用户是否存在
    data = db_api("select * from accounts where account=%s" % account)
    """
    data 返回的数据体 
    {"balance": 752.5499999999884, "expire_date": "2021-01-01", "enroll_date": "2016-01-02", 
    "credit": 15000, "id": 1234, "status": 0, "pay_day": 22, "password": "abc"
    }
    """
    if data['password'] == password:
        # 将文件中的字符串时间转换为结构化时间后，再转换为时间戳
        exp_time_stamp = time.mktime(time.strptime(data['expire_date'], "%Y-%m-%d"))
        # 当前时间戳是否 大于 账号的过期时间
        if time.time() > exp_time_stamp:
            # 账号已过期
            print("\033[31;1mAccount [%s] has expired,please contact the back to get a new card!\033[0m" % account)
        else:  # passed the authentication
            # 账号未过期,并返回用户的数据
            return data
    else:
        print("\033[31;1mAccount ID or password is incorrect!\033[0m")


def acc_login(user_data, log_obj):
    """
    account login func
    :user_data: user info data , only saves in memory
    :return:
    """
    retry_count = 0
    while user_data['is_authenticated'] is not True and retry_count < 3:  # is_authenticated 为假,并且重试次数小于3
        account = input("\033[32;1m account:\033[0m").strip()  # 用户名
        password = input("\033[32;1m password:\033[0m").strip()  # 用户密码
        auth = acc_auth2(account, password)
        if auth:  # not None means passed the authentication
            user_data['is_authenticated'] = True  # 修改用户登录状态
            user_data['account_id'] = account  # 将None 修改为用户输入的名字
            return auth  # 返回文件中的数据
        retry_count += 1
    else:
        log_obj.error("account [%s] too many login attempts" % account)
        exit()
