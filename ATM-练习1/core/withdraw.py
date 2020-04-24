# _*_ coding; utf-8 _*_
# author: cc
#

"""
1. 选择1 账户信息 显示alex的当前账户余额和信用额度。
2. 选择2 提现 提现金额应小于等于信用额度，利息为5%，提现金额为用户自定义。
"""
import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

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


def withdrawalStart(balance, creditLimit, withdrawalAmount):
    """
    提现
    :param balance: 账户余额
    :param creditLimit: 信用卡额度
    :param withdrawalAmount: 提现金额
    :return:
    """
    msg = """--------- ICBC Bank ----------
    1.  账户信息
    2.  提现"""
    username = 'alex'
    rootPath = r'%s\account' % BASE_DIR
    userFilePath = r'%s\%s.json' % (rootPath, username)  # alex 账号文件
    # 写入账户余额和信用卡额度
    updateFileDate(userFilePath, {'balance': balance, 'creditLimit': creditLimit})
    while True:
        print(msg)
        choice = input("input choice: ")
        if choice and choice.isdigit():
            choice_id = int(choice)
            if 2 >= choice_id > 0:
                # 读取文件中的数据
                alex_account = loadFileData(userFilePath)
                if choice_id == 1:
                    # 查看余额和信用额度
                    print('username: %s, account_balance: %d, credit Limit: %d'
                          % (username, alex_account['account_balance'], alex_account['creditLimit']))
                elif choice_id == 2:
                    # 提现
                    amountSum = withdrawalAmount + (withdrawalAmount * 0.05)
                    if amountSum <= alex_account['creditLimit']:
                        # 提现后的金额=当前余额+提现金额
                        alex_account['account_balance'] += withdrawalAmount
                        # 提现后信用额度=当前账户信用额度-提现金额-利息
                        alex_account['creditLimit'] -= amountSum
                        print('账户余额: %d, 信用卡剩余可用额度: %d, 提现%d 到账户中'
                              % (alex_account['account_balance'], alex_account['creditLimit'], withdrawalAmount))
                        # 更改账户信息
                        return updateFileDate(userFilePath, alex_account)
                    else:
                        print('信用卡额度不够')
            else:
                print('choice id %d not exists.' % choice_id)


if __name__ == '__main__':
    withdrawalStart(1000000, 30000, 1000)
