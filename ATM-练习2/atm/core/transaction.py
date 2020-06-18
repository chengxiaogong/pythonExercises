#!_*_coding:utf-8_*_
#__author__:"Alex Li"

from conf import settings
from core import accounts


def make_transaction(log_obj, account_data, tran_type, amount, **others):
    """
    deal all the user transactions
    :param log_obj: 日志对象
    :param account_data: user account data  用户数据
    :param tran_type: transaction type   repay
    :param amount: transaction amount  金额
    :param others: mainly for logging usage
    :return:
    """
    amount = float(amount)
    if tran_type in settings.TRANSACTION_TYPE:
        # 手续费
        interest = amount * settings.TRANSACTION_TYPE[tran_type]['interest']
        old_balance = account_data['balance']
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            # 加
            new_balance = old_balance + amount + interest
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            # 减
            new_balance = old_balance - amount - interest
            if others.get('transfer_account'):
                # 加载转账用户中的数据
                transfer_account = accounts.load_current_balance(others.get('transfer_account'))
                # 转入到对方账户中,把钱给它转过去
                transfer_account['balance'] += amount
                # 保存数据
                accounts.dump_account(transfer_account)
            # check credit
            if new_balance < 0:
                print('''\033[31;1mYour credit [%s] is not enough for this transaction [-%s], your current balance is
                [%s]''' % (account_data['credit'], (amount + interest), old_balance))
                return
        account_data['balance'] = new_balance  # 修改余额
        accounts.dump_account(account_data)  # save the new balance back to file
        log_obj.info("account:%s   action:%s    amount:%s   interest:%s" %
                     (account_data['id'], tran_type, amount, interest))
        return account_data
    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m" % tran_type)
