# -*- coding: utf-8 -*-
# 


"""
主逻辑交互程序
"""

from core import logger
from core import auth
from core.auth import login_check
from core import accounts
from core import transaction
from sys import path as sys_path
from os import path as os_path

# 交易日志对象
transaction_log = logger.log_func('transaction')
# 访问日志对象
access_log = logger.log_func('access')

# 初始化默认数据
user_data = {
    'account_id': None,
    'is_authenticated': False,
    'account_data': None
}

"""
装饰器登录验证过程
account_info = auth.login_check(account_info)
account_info(acc_data)
需要注意的是: acc_data 是一个字典, inner(*args, **kwargs) , 这样将acc_data 传递给inner 就相当于作为args 元组中的第一个元素
而不是一个字典,所以inner 中需要通过 args[0] 这样来取这个字典
"""


@login_check
def account_info(acc_data):
    # 查看账号信息
    account_data = accounts.load_current_balance(acc_data['account_id'])
    print(account_data)


@login_check
def repay(acc_data):
    """
    还款功能
    :param acc_data: 用户数据
    :return:
    """
    # 实时获取用户数据,保证数据是最新的
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    flag = False
    while not flag:
        # 输入还款金额
        repay_amount = input("Enter repayment amount: ").strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            new_balance = transaction.make_transaction(transaction_log, account_data, 'repay', repay_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif repay_amount == 'b':
            flag = True
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)


@login_check
def withdraw(acc_data):
    # 取款
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    flag = False
    while not flag:
        # 输入取款金额
        withdraw_money = input("Enter withdrawal amount: ").strip()
        if len(withdraw_money) > 0 and withdraw_money.isdigit():
            new_balance = transaction.make_transaction(transaction_log, account_data, 'withdraw', withdraw_money)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif withdraw_money == 'b':
            flag = True
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_money)


@login_check
def transfer(acc_data):
    # 转账
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    flag = False
    while not flag:
        # 输入转账卡号(账号)
        transfer_account = input("Enter transfer account: ")
        # 输入转账金额
        transfer_money = input("Enter transfer money: ")
        if (len(transfer_money) > 0 and transfer_money.isdigit()) and len(transfer_account) > 0:
            # 这里使用**kwargs 扩展参数, transfer_account 根据这个dict key判断是否需要转账
            new_balance = transaction.make_transaction(transaction_log, account_data, 'transfer', transfer_money,
                                                       transfer_account=transfer_account)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif transfer_account == 'b' or transfer_money == 'b':
            flag = True
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % transfer_account)


@login_check
def login_exit(acc_data):
    print(acc_data, '注销')
    exit()


def interactive(acc_data):
    """
    用户交互
    :param acc_data: 用户数据
    :return:
    """
    menu_dict = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': login_exit
    }
    menu = u'''
    ------- 银行卡操作 ---------
    \033[32;1m1.  账户信息
    2.  还款
    3.  取款
    4.  转账
    5.  退出
    \033[0m'''
    flag = False
    while not flag:
        print(menu)
        user_option = input("input option: ")
        # 映射
        if user_option in menu_dict:
            """
            men_dict[user_option] 相当于就是获取到了功能函数的内存地址,但是并没有直接运行
            例如: 输入的是2, 还款, 那么就是 men_dict[2](acc_data)
            这样的好处就不用写if ... else 来做判断了
            """
            menu_dict[user_option](acc_data)
        else:
            print('option not exists')

        if flag == 'b':
            flag = True


def shopping_mall_all(acc_data):
    menu = u'''
    ------- 商城购物 ---------
    \033[32;1m1.  客户端
    2.  管理端
    \033[0m'''
    print(sys_path)
    sys_path.append(os_path.dirname(sys_path[-1]))
    from shopping_mall import shopping_mall
    menu_dict = {
        '1': shopping_mall.user_shopping(acc_data),
        '2': shopping_mall.business()
    }
    print(menu)
    user_option = input("input option: ")
    if user_option in menu_dict:
        result = menu_dict[user_option]
        print(result)
    else:
        print('option not exists.')


def user_interaction(acc_data):
    """
    用户交互中心
    :param acc_data: 用户数据
    :return:
    """
    menu = u'''
    ------- 用户交互中心 ---------
    \033[32;1m1.  ATM终端
    2.  商城购物
    \033[0m'''
    menu_dict = {
        '1': interactive,
        '2': shopping_mall_all
    }
    flag = False
    while not flag:
        print(menu)
        user_option = input("input option: ")
        if user_option in menu_dict:
            menu_dict[user_option](acc_data)
        elif user_option == 'b':
            flag = True
        else:
            print('option not exists.')


def run():
    print(user_data)  # user_data = {'account_id': None,'is_authenticated': False,'account_data': None}
    acc_data = auth.user_login(user_data, access_log)
    if acc_data:
        user_data['account_data'] = acc_data
        print(user_data)
        # interactive(user_data)
        user_interaction(user_data)
