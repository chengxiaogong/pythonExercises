# -*- coding: utf-8 -*-
# 

"""
用于从文件里加载和存储账户数据
"""

from core import db_handler


def load_current_balance(account_id):
    """
    查看账号的当前余额
    :param account_id:
    :return:
    """
    db_api = db_handler.db_handler()
    account_data = db_api('select * from accounts where account=%s' % account_id)
    return account_data


def dumps_account(account_data):
    db_api = db_handler.db_handler()
    db_api('update accounts where account=%s' % account_data['id'], account_data=account_data)
