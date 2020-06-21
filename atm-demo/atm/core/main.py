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
account_info = auth.login_check(account_info)
account_info(acc_data)
"""


@login_check
def account_info(acc_data):
    # 查看账号信息
    account_data = accounts.load_current_balance(acc_data['account_id'])
    print(account_data)


@login_check
def repay(acc_data):
    # 还款
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    flag = False
    while not flag:
        repay_amount = input("Enter repayment amount: ").strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            new_balance = transaction.make_transaction(transaction_log, account_data, 'repay', repay_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)
        if repay_amount == 'b':
            flag = True


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
        withdraw_money = input("Enter withdrawal amount: ").strip()
        if len(withdraw_money) > 0 and withdraw_money.isdigit():
            new_balance = transaction.make_transaction(transaction_log, account_data, 'withdraw', withdraw_money)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_money)

        if withdraw_money == 'b':
            flag = True


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
        transfer_account = input("Enter transfer account: ")
        transfer_money = input("Enter transfer money: ")
        if (len(transfer_money) > 0 and transfer_money.isdigit()) and len(transfer_account) > 0:
            new_balance = transaction.make_transaction(transaction_log, account_data, 'transfer', transfer_money,
                                                       transfer_account=transfer_account)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % transfer_account)

        if transfer_account == 'b' or transfer_money == 'b':
            flag = True


@login_check
def login_exit(acc_data):
    print(acc_data, '注销')
    exit()


def interactive(acc_data):
    # 用户交互
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
        if user_option in menu_dict:
            menu_dict[user_option](acc_data)
        else:
            print('option not exists')

        if flag == 'b':
            flag = True


def run():
    print(user_data)
    acc_data = auth.user_login(user_data, access_log)
    if acc_data:
        user_data['account_data'] = acc_data
        print(user_data)
        interactive(user_data)
