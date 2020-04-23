# _*_ coding; utf-8 _*_
# author: cc
#

import sys
import os
import json


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

"""
需求1:
最近alex买了个Tesla Model S，通过转账的形式，并且支付了5%的手续费，tesla价格为95万。
账户文件为json，请用程序实现该转账行为。

1. 选择1 账户信息 显示alex的当前账户余额。
2. 选择2 转账 直接扣掉95万和利息费用并且tesla_company账户增加95万

需求2:
1. 选择3 账户信息 显示alex的当前账户余额和信用额度。
2. 选择4 提现 提现金额应小于等于信用额度，利息为5%，提现金额为用户自定义。
3. 体现代码的实现要写在withdraw.py里
"""


def transferAccounts(srcAccount, destAccount, commodityPrice):
    """
    转账
    :param srcAccount: 源账号
    :param destAccount: 目标账号(需要转入的账号)
    :param commodityPrice: 商品价格
    :return:
    """
    serviceCharge = 0.05  # 手续费5%
    price = commodityPrice + (commodityPrice * serviceCharge)
    if srcAccount['account_balance'] >= price:
        # 从alex账户中扣钱,包含手续费
        srcAccount['account_balance'] -= price
        # 将钱转到 tesla_company 账户中,但是不包含手续费,手续费是由银行收取了
        destAccount['account_balance'] += commodityPrice
        print('alex 购买了一台特斯拉,手续费和特斯拉合计扣除: %d, 特斯拉公司收到转账: %d, 所需手续费: %d'
              % (price, commodityPrice, commodityPrice * serviceCharge))
        return updateFileDate(userFilePath, srcAccount), updateFileDate(companyFilePath, destAccount)
    else:
        print('余额不够,快去挣钱吧!!!')


def loadFileData(filePath):
    # 加载文件中的数据
    with open(filePath, 'r') as fileObj:
        return json.load(fileObj)


def updateFileDate(filePath, content):
    """
    修改文件中的数据
    :param filePath: 文件名
    :param content: 内容
    :return:
    """
    with open(filePath, 'w') as fileObj:
        return json.dump(content, fileObj)


if __name__ == '__main__':
    msg = """--------- ICBC Bank ----------
1.  账户信息
2.  转账"""
    username = 'alex'
    rootPath = r'%s\account' % BASE_DIR
    userFilePath = r'%s\%s.json' % (rootPath, username)
    companyFilePath = r'%s\%s.json' % (rootPath, 'tesla_company')
    while True:
        print(msg)
        choice = input("input choice: ")
        if choice and choice.isdigit():
            choice_id = int(choice)
            if 2 >= choice_id > 0:
                users_info = loadFileData(userFilePath)
                company_info = loadFileData(companyFilePath)
                if choice_id == 1:
                    # 查看余额和信用额度
                    print('username: %s, balance: %d, credit limit: %d'
                          % (username, users_info['account_balance'], users_info['credit_account']))
                elif choice_id == 2:
                    # 转账
                    transferAccounts(users_info, company_info, 950000)
            else:
                print('choice id %d not exists.' % choice_id)

