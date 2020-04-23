# _*_ coding; utf-8 _*_
# author: cc
#

"""
1. 选择1 账户信息 显示alex的当前账户余额和信用额度。
2. 选择2 提现 提现金额应小于等于信用额度，利息为5%，提现金额为用户自定义。
"""



def cashWithdrawal(users):
    # 提现
    serviceCharge = 0.05  # 手续费5%
    withdrawalAmount = input("提现金额: ")
    if withdrawalAmount and withdrawalAmount.isdigit():
        amount = int(withdrawalAmount)
        serviceChargeToBePaid = amount * (amount + serviceCharge)
        if amount <= users['credit_limit']:
            if users['balance'] >= serviceChargeToBePaid:
                print('提现前: %d' % users['credit_limit'])
                users['credit_limit'] -= serviceChargeToBePaid
                print('提现后: %d' % users['credit_limit'])
            else:
                print('余额不足')
                print('您的账户余额为: %d' % users['balance'])
        else:
            print('提现金额超出信用额度')




if __name__ == '__main__':
    dic = {"expire_date": "2021-10-02", "id": 1, "status": 0, "pay_day": 22, "password": "e99a18c428cb38d5f260853678922e03", "balance": 1000000, "credit_limit":  30000}
    cashWithdrawal(dic)
