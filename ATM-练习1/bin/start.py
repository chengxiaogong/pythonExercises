# _*_ coding; utf-8 _*_
# author: cc
#

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import fileManager
from core import auth
"""
需求1:
最近alex买了个Tesla Model S，通过转账的形式，并且支付了5%的手续费，tesla价格为95万。
账户文件为json，请用程序实现该转账行为。

1. 选择1 账户信息 显示alex的当前账户余额。
2. 选择2 转账 直接扣掉95万和利息费用并且tesla_company账户增加95万
"""

@auth.login
def transferAccounts(alexBalance, teslaMoney):
    """
    转账
    :param alexBalance: alex 账户余额
    :param teslaMoney: 购买特斯拉需要多少钱
    :return:
    """
    username = 'alex'
    rootPath = r'%s\account' % BASE_DIR
    userFilePath = r'%s\%s.json' % (rootPath, username)  # alex 账号文件
    teslaFilePath = r'%s\%s.json' % (rootPath, 'tesla_company')  # 特斯拉账号文件
    # 将余额写入到 alex 账户文件中
    fileManager.updateFileDate(userFilePath, {'account_balance': alexBalance})
    while True:
        msg = """--------- ICBC Bank ----------
        1.  账户信息
        2.  转账"""
        print(msg)
        choice = input("input choice: ")
        if choice and choice.isdigit():
            choice_id = int(choice)
            if 2 >= choice_id > 0:
                # 读取文件中的数据
                alex_account = fileManager.loadFileData(userFilePath)
                tesla_account = fileManager.loadFileData(teslaFilePath)
                if choice_id == 1:
                    # 查看余额
                    print('username: %s, account_balance: %d' % (username, alex_account['account_balance']))
                elif choice_id == 2:
                    # 转账
                    teslaPrice = teslaMoney + (teslaMoney * 0.05)  # 特斯拉+税后
                    print('特斯拉价格: %s' % teslaPrice)
                    if alex_account['account_balance'] >= teslaPrice:
                        # 从alex账户中扣钱,包含手续费
                        alex_account['account_balance'] -= teslaPrice
                        # 将钱转到 tesla_company 账户中,但是不包含手续费,手续费是由银行收取了
                        tesla_account['account_balance'] += teslaMoney
                        print('%s 特斯拉和税后合计扣除: %d, 账户余额: %d , 特斯拉公司收到转账: %d, 所需手续费: %d'
                              % (username, teslaPrice, alex_account['account_balance'] , teslaMoney, teslaMoney * 0.05))
                        # 将变更后的数据写入到文件中
                        return fileManager.updateFileDate(userFilePath, alex_account),\
                               fileManager.updateFileDate(teslaFilePath, tesla_account)
                    else:
                        print('余额不够,还差%d' % (teslaPrice - alex_account['account_balance']))
            else:
                print('choice id %d not exists.' % choice_id)


if __name__ == '__main__':
    login_status = False
    transferAccounts(1000000, 950000)
