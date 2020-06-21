# -*- coding: utf-8 -*-
# 

"""
记账,还钱,取钱等所有的与账户金额相关的操作都在这
"""

from conf import settings
from core import accounts


def make_transaction(log_obj, account_data, tran_type, money, **kwargs):
    """
    交易
    :param log_obj: 日志对象
    :param account_data: 用户账号数据
    :param tran_type: 交易类型
    :param money: 金额
    :param kwargs: 扩展参数
    :return:
    """
    money = float(money)
    transaction_type = settings.TRANSACTION_TYPE
    if tran_type in transaction_type:
        # 计算利息
        old_balance = account_data['balance']
        interest = money * transaction_type[tran_type]['interest']
        if transaction_type[tran_type]['action'] == 'plus':
            print('加法')
            new_balance = old_balance + money + interest
        elif transaction_type[tran_type]['action'] == 'minus':
            print('减法')
            new_balance = old_balance - money - interest
            if kwargs.get('transfer_account'):
                transfer_account_data = accounts.load_current_balance(kwargs.get('transfer_account'))
                # 转入到对方账户中
                transfer_old_balance = transfer_account_data['balance']
                transfer_new_balance = transfer_old_balance + money
                transfer_account_data['balance'] = transfer_new_balance
                # 将数据保存到文件中
                accounts.dumps_account(transfer_account_data)
            # 效验余额是否不足?
            if new_balance < 0:
                print('''\033[31;1mYour credit [%s] is not enough for this transaction [-%s], your current balance is
                                [%s]''' % (account_data['credit'], (money + interest), old_balance))
                return
        account_data['balance'] = new_balance
        accounts.dumps_account(account_data)
        log_obj.info("account:%s   action:%s    amount:%s   interest:%s" %
                     (account_data['id'], tran_type, money, interest))
        return account_data
    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m" % tran_type)
