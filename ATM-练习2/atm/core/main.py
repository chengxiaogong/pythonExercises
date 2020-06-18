#!_*_coding:utf-8_*_
#__author__:"Alex Li"

'''
main program handle module , handle all the user interaction stuff

'''

from core import auth
from core import logger
from core import accounts
from core import transaction
from core.auth import login_required
from shopping_mall import shopping_mall


# transaction logger
trans_logger = logger.logger('transaction')
# access logger
access_logger = logger.logger('access')


# temp account data ,only saves the data in memory
user_data = {
    'account_id': None,
    'is_authenticated': False,
    'account_data': None

}


@login_required
def account_info(acc_data):
    print(acc_data)


@login_required
def repay(acc_data):
    """
    print current balance and let user repay the bill
    :return:
    """
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        repay_amount = input("\033[33;1mInput repay amount:\033[0m").strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            print('ddd 00')
            new_balance = transaction.make_transaction(trans_logger, account_data, 'repay', repay_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))

        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)

        if repay_amount == 'b':
            back_flag = True


@login_required
def withdraw(acc_data):
    """
    print current balance and let user do the withdraw action
    :param acc_data:
    :return:
    """
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[33;1mInput withdraw amount:\033[0m").strip()
        if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'withdraw', withdraw_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)

        if withdraw_amount == 'b':
            back_flag = True


@login_required
def transfer(acc_data):
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        transfer_in_Account_No = input("\033[33;1mInput transfer account:\033[0m").strip()
        transfer_amount = input("\033[33;1mInput transfer amount:\033[0m").strip()
        print(transfer_amount, transfer_in_Account_No)
        if len(transfer_amount) > 0 and transfer_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'transfer', transfer_amount,
                                                       transfer_account=transfer_in_Account_No)
            if new_balance:
                print('\033[31;1mNew Balance: %s\033[0m' % new_balance['balance'])
        else:
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % transfer_amount)

        if transfer_in_Account_No == 'b':
            back_flag = True


def pay_check(acc_data):
    pass  # todo


def logout(acc_data):
    exit('Bye Bye...')


@login_required
def mall(acc_data):
    choice = input("\033[31;1m 您是商家? \033[0m").strip()
    if choice == 'y':
        shopping_mall.business()
    else:
        shopping_mall.userShopping(acc_data)


def interactive(acc_data):
    """
    interact with user
    :return:
    """
    menu = u'''
    ------- 银行卡操作 ---------
    \033[32;1m1.  账户信息
    2.  还款(功能已实现)
    3.  取款(功能已实现)
    4.  转账(功能已实现)
    5.  账单
    6.  退出
    \033[0m'''
    menu_dic = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': pay_check,
        '6': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            print('acc_data', acc_data)
            menu_dic[user_option](acc_data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def main_menu(acc_data):
    mainMenu = u'''
    ----------主菜单---------
    \033[32;1m
    1.购物商城
    2.银行卡操作
    3.退出
    \033[0m
    '''
    main_menu_dic = {
        '1': mall,
        '2': interactive,
        '3': logout
    }
    back_flag = False
    while not back_flag:
        print(mainMenu)
        user_option = input(">>:").strip()
        if user_option == 'b':
            return
        if user_option in main_menu_dic:
            main_menu_dic[user_option](acc_data)
        else:
            print('\033[31;1m选择不存在! \033[0m')


def run():
    """
    this function will be called right a way when the program started, here handles the user interaction stuff
    :return:
    """
    # user_data = {'account_id':None, 'is_authenticated':False, 'account_data':None}
    print(user_data)
    acc_data = auth.acc_login(user_data, access_logger)
    if user_data['is_authenticated']:  # 登录成功时,这里的状态会为True
        user_data['account_data'] = acc_data  # 得到用户文件存储中的数据
        main_menu(user_data)
