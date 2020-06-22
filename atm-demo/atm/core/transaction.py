# -*- coding: utf-8 -*-
# 

"""
记账,还钱,取钱等所有的与账户金额相关的操作都在这
"""

from conf import settings
from core import accounts


def make_transaction(log_obj, account_data, tran_type, money, **kwargs):
    """
    交易中心
    :param log_obj: 日志对象
    :param account_data: 用户账号数据
    :param tran_type: 交易类型
    :param money: 金额
    :param kwargs: 扩展参数
    :return:
    """
    money = float(money)
    transaction_type = settings.TRANSACTION_TYPE
    # 效验交易类型是否在字典中存在
    if tran_type in transaction_type:
        # 之前的余额
        old_balance = account_data['balance']
        # 计算利息
        interest = money * transaction_type[tran_type]['interest']
        if transaction_type[tran_type]['action'] == 'plus':
            print('加法')
            new_balance = old_balance + money + interest  # 余额+金额+利息
        elif transaction_type[tran_type]['action'] == 'minus':
            print('减法')
            new_balance = old_balance - money - interest  # 余额-金额-利息
            if kwargs.get('transfer_account'):
                # 转账人的卡号信息
                transfer_account_data = accounts.load_current_balance(kwargs.get('transfer_account'))
                # 转入到对方账户中
                transfer_old_balance = transfer_account_data['balance']
                transfer_new_balance = transfer_old_balance + money  # 对方账户余额+转入金额
                transfer_account_data['balance'] = transfer_new_balance
                # 将数据保存到文件中
                accounts.dumps_account(transfer_account_data)
            # 效验余额是否不足?
            if new_balance < 0:
                print('''\033[31;1mYour credit [%s] is not enough for this transaction [-%s], your current balance is
                                [%s]''' % (account_data['credit'], (money + interest), old_balance))
                return
        # 更新用户余额
        account_data['balance'] = new_balance
        # 将数据保存到文件中
        accounts.dumps_account(account_data)
        # 记录交易日志
        log_obj.info("account:%s   action:%s    amount:%s   interest:%s" %
                     (account_data['id'], tran_type, money, interest))
        # 返回用户数据
        return account_data
    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m" % tran_type)
