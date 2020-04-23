# _*_ coding; utf-8 _*_
# author: cc
#

"""
写一个用户登录验证程序，文件名account.json，内容如下
{“expire_date”: “2021-01-01”, “id”: 1234, “status”: 0, “pay_day”: 22, “password”: “abc”}

1. 根据用户输入的用户名&密码，找到对应的json文件，把数据加载出来进行验证
2. 用户名为json文件名，密码为 password。
3. 判断是否过期，与expire_date进行对比。
4. 登陆成功后，打印“登陆成功”，三次登陆失败，status值改为1，并且锁定账号。
5. 用户密码进行hashlib加密处理。即：json文件里的密码保存为md5的值，然后用md5的值进行验证账号信息是否正确
"""

import json
import time
import os
import hashlib


def writeTestData(userName, userId, payDay, password, status=0, expire_data='2021-05-02'):
    """
    写入测试数据
    :param id: 用户id
    :param status: 用户状态,1表示连续三次登录失败,已锁定改账户, 0表示正常
    :param pay_day: 发薪日
    :param password: 账户密码
    :param expire_data: 账户的过期时间
    :return:
    """
    content = {
        'expire_date': expire_data,
        'id': userId,
        'status': status,
        'pay_day': payDay,
        'password': encryptionProcessing(password)  # 写入文件中的密码做md5加密处理
    }
    with open('%s/%s.json' % (filePath, userName), 'w', encoding='utf-8') as fileObj:
        json.dump(content, fileObj)


def loadUserData():
    # 加载数据
    with open(filePath, 'r') as fileObj:
        return json.load(fileObj)


def lockUser():
    # 锁定用户
    with open(filePath, 'w') as fileObj:
        return json.dump(users, fileObj)


def userLogin():
    # 用户登录
    for i in range(1, 4):
        password = input('input user password: ')
        if encryptionProcessing(password) == users['password']:
            print('user %s login success' % username)
            return True
        else:
            print('user %s login fail' % username)
    # 修改用户状态
    users['status'] = 1


def checkUserIsLocket(fun):
    # 验证账号有没有锁定
    if users['status'] == 1:
        print('user %s is locket' % username)
    else:
        # 登录失败,锁定用户
        if not fun():
            print('连续三次登录失败，该用户 %s 已锁定' % username)
            lockUser()


def encryptionProcessing(string):
    # md5加密
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()


if __name__ == '__main__':
    # 写入测试数据
    filePath = './files'
    # if not os.path.exists(filePath):
    #     os.mkdir(filePath)
    # writeTestData('qq', 2, 22, 'abc123')

    username = input("input user name: ")
    if username:
        filePath = './files/%s.json' % username
        if os.path.exists(filePath):
            users = loadUserData()
            currentDate = time.strftime('%Y-%m-%d')
            # 效验账号有没有过期
            if users['expire_date'] < currentDate:
                # 账号已过期
                print('%s account expired' % username)
            else:
                # 账号未过期
                checkUserIsLocket(userLogin)
        else:
            print('user %s file not exists' % username)
