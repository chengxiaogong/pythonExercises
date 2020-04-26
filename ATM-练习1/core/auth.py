# _*_ coding; utf-8 _*_
# author: cc
#

import sys
import os
import time
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import fileManager


def encryptionProcessing(string):
    # md5加密
    if string:
        md5 = hashlib.md5()
        md5.update(string.encode())
        return md5.hexdigest()


def login(functionName):
    def inner(*args, **kwargs):
        """
        登录验证装饰器
        :param args:
        :param kwargs:
        :return:
        """
        username = input("input user name: ")
        fileName = ".".join([username, "json"])
        filePath = os.path.join(BASE_DIR, "account", fileName)
        if os.path.exists(filePath):
            account_info = fileManager.loadFileData(filePath)
            # 获取当前的时间戳
            currentTime = time.time()
            # 将字符串时间转换为时间戳
            structTime = time.strptime(account_info['expire_date'], '%Y-%m-%d')
            # 将结构化时间转换为时间戳
            expireDate = time.mktime(structTime)
            if account_info['login_status'] is False:
                # 计时器
                login_count = 1
                flag = True
                while flag:
                    if account_info['status'] == 1:
                        print('账号已锁定', username)
                        flag = False
                    else:
                        password = encryptionProcessing(input("input user password: "))
                        if password and account_info['password'] == password:
                            # 登录成功了,验证账号有没有过期
                            if currentTime < expireDate:
                                # 更改用户的登录状态
                                account_info['login_status'] = True
                                print('%s user login success!!!' % username)
                                flag = False
                            else:
                                print('账号已过期')
                                flag = False
                        else:
                            print('%s user login failed' % username)
                            if login_count == 3:
                                print('三次登录失败,锁定该账户', username)
                                account_info['status'] = 1
                                flag = False
                            login_count += 1
            # 更新文件内容
            fileManager.updateFileDate(filePath, account_info)
            if account_info['login_status']:
                functionName(*args, **kwargs)
        else:
            print('用户不存在', username)
    return inner

