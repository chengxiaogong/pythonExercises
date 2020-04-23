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
    amount = input("提现金额: ")
    if amount and amount.isdigit():
        amount = int(amount)
        amount_sum = amount + (amount * serviceCharge)
        if users['credit_account'] >= amount_sum:
            users['account_balance'] -= amount_sum
            users['credit_account'] -= amount_sum
            print('剩余账户余额: %d, 剩余信用卡额度: %d, 已扣除: %d'
                  % (users['account_balance'], users['credit_account'], amount_sum))
        else:
            print('信用卡额度不够')
    return users


if __name__ == '__main__':
    dic = {"expire_date": "2021-10-02", "id": 1, "status": 0, "pay_day": 22,
           "password": "e99a18c428cb38d5f260853678922e03", "account_balance": 1000000, "credit_account": 30000}
    cashWithdrawal(dic)
