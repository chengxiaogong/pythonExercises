# -*- coding:utf-8 -*-
# __author__: cc

import os
from core import accounts


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, 'shopping_mall', 'product.txt')


def getCommodityData():
    # 获取商品数据
    print(BASE_DIR)
    shopping_list = []
    with open(FILE_PATH, 'r', encoding='utf-8') as fileObj:
        fileContent = fileObj.readlines()
        for item in fileContent:
            name, price = item.strip('\n').split(':')
            shopping_list.append([name.strip(), int(price.strip())])
    return shopping_list


def storageCommodityData(product):
    fileObj = open(FILE_PATH, 'w', encoding='utf-8')
    for item in product:
        item[1] = str(item[1])
        line = ':'.join(item)
        fileObj.write(line + '\n')


def deductMoney(account_data, commodity):
    """
    扣钱
    :param account_data: 用户数据
    :param commodity: 商品信息
    :return dict:
    """
    if account_data['balance'] >= commodity[1]:
        account_data['balance'] -= commodity[1]
        print('commodityName: %s, commodityPrice: %d, accountBalance: %d' % (
            commodity[0], commodity[1], account_data['balance']
        ))
        return account_data
    elif account_data['credit'] >= commodity[1]:
        account_data['credit'] -= commodity[1]
        print('commodityName: %s, commodityPrice: %d, accountCredit: %d' % (
            commodity[0], commodity[1], account_data['credit']
        ))
        return account_data
    else:
        print('余额不足,快去挣钱吧!!!')


def userShopping(account_data):
    """
    用户购物
    :param account_data: 用户数据
    :return:
    """
    product = getCommodityData()
    user_data = account_data.get('account_data')
    current_balance = ''' --------- 当前余额 --------
        Credit :    %s
        Balance:    %s''' % (user_data['credit'], user_data['balance'])
    print(current_balance)
    # 初始化变量
    flag, shoppingCart = False, []
    while not flag:
        # 初始化商品id
        commodityId = 1
        print('product list: ')
        for item in product:
            print('product id: %d, product name: %s, product price: %d' % (commodityId, item[0], item[1]))
            commodityId += 1
        user_option = input("\033[33;1mInput commodity id: \033[0m").strip()
        if len(user_option) >= 1 and user_option.isdigit():
            commodityID = int(user_option)
            # 检查商品是否存在
            if commodityID <= len(product) >= commodityID != 0:
                # 扣钱, 存蓄卡有钱,就从存蓄卡里扣除,存蓄卡里没有钱就扣信用卡
                if deductMoney(user_data, product[commodityID - 1]):
                    shoppingCart.append(product[commodityID - 1])
            else:
                print('commodity id %d not exists' % commodityID)
        elif user_option == 'b':
            if len(shoppingCart) >= 1:
                current_balance = ''' --------- 消费后的余额 --------
                    Credit :    %s
                    Balance:    %s''' % (user_data['credit'], user_data['balance'])
                print(current_balance)
                print('-------------购物清单--------------')
                for item in shoppingCart:
                    print('commodityName: %s, commodityPrice: %d' % (item[0], item[1]))
                accounts.dump_account(user_data)
            else:
                print('shopping cart is null')
            flag = True


def business():
    # 商家
    product = getCommodityData()
    choice = input("\033[31;1m Input operation type: [add|modify] \033[0m")
    if choice == 'add':
        commodityName = input("输入需要添加的商品名称: ").strip()
        commodityPrice = input("输入需要添加的商品价格: ").strip()
        if commodityName and commodityPrice.isdigit():
            product.append([commodityName, int(commodityPrice)])
            for item in product:
                print(item)
            storageCommodityData(product)
            print('add commodity %s success' % commodityName)
    elif choice == 'modify':
        commodityName = input("输入需要修改的商品名称: ").strip()
        commodityPrice = input("输入需要修改的商品价格: ").strip()
        if commodityName and commodityPrice.isdigit():
            items, count = {}, 0
            for item in product:
                name = item[0]
                if name == commodityName:
                    item[1] = int(commodityPrice)
                    items = {'name': item[0], 'price': item[1], 'index': count}
                count += 1
            if len(items) != 0:
                oldPrice = product[items['index']]
                # update commodity price
                product[items['index']] = [items['name'], items['price']]
                print('commodity name: %s, commodity old price %s, commodity new price %s' %
                      (commodityName, oldPrice, commodityPrice))
                for item in product:
                    print(item)
                storageCommodityData(product)
            else:
                print('没有这个商品')


if __name__ == '__main__':
    acc_data = {"balance": 100, "expire_date": "2021-01-01", "enroll_date": "2016-01-02", "credit": 15000, "id": 1234,
                "status": 0, "pay_day": 22, "password": "abc"}
    userShopping(acc_data)
