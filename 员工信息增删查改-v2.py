# -*- coding; utf-8 -*-
# __author__: cc
#

"""
需求:
语法操作：
1.可进行模糊查询:
    find name,age from staff_table where age > 22
    find * from staff_table where dept = "IT"
    find * from staff_table where enroll_date like "2013"
2.可创建新员工纪录，以phone做唯一键(即不允许表里有手机号重复的情况)，staff_id需自增
    语法: add staff_table Alex Li,18,134435344,IT,2015-10-29
3.可删除指定员工信息纪录，输入员工id，即可删除
    语法: del from staff_tables where  id=3
4.可修改员工信息，语法如下:
    UPDATE staff_table SET dept = "Market" WHERE  dept = "IT" 把所有dept=IT的纪录的dept改成Market
    UPDATE staff_table SET age = 25 WHERE  name = "Alex Li"  把name=Alex Li的纪录的年龄改成25
"""

import os
from tabulate import tabulate


def initializeBasicData():
    # 写入基础数据,用于测试使用
    data = """1,Alex Li,22,13651054608,IT,2013-04-01
2,Jack Wang,28,13451024608,HR,2015-01-07
3,Rain Wang,21,13451054608,IT,2017-04-01
4,Mack Qiao,44,15653354208,Sales,2016-02-01
5,Rachel Chen,23,13351024606,IT,2013-03-16
6,Eric Liu,19,18531054602,Marketing,2012-12-01
7,Chao Zhang,21,13235324334,Administration,2011-08-08
8,Kevin Chen,22,13151054603,Sales,2013-04-01
9,Shit Wen,20,13351024602,IT,2017-07-03
10,Shanshan Du,26,13698424612,Operation,2017-07-02"""
    if not os.path.exists(filePath):
        # 创建家目录
        if not os.path.exists(rootPath):
            os.mkdir(rootPath)
        # 写入基础数据到文件中
        with open(filePath, 'w', encoding='utf-8') as fileObj:
            fileObj.write(data)


def help():
    msg = """语法操作：
1.可进行模糊查询:
    find name,age from staff_table where age > 22
    find * from staff_table where dept = "IT"
    find * from staff_table where enroll_date like "2013"
2.可创建新员工纪录，以phone做唯一键(即不允许表里有手机号重复的情况)，staff_id需自增
    语法: add staff_table Alex Li,18,134435344,IT,2015-10-29  
3.可删除指定员工信息纪录，输入员工id，即可删除
    语法: del from staff_tables where  id=3
4.可修改员工信息，语法如下:
    UPDATE staff_table SET dept = "Market" WHERE  dept = "IT" 把所有dept=IT的纪录的dept改成Market
    UPDATE staff_table SET age = 25 WHERE  name = "Alex Li"  把name=Alex Li的纪录的年龄改成25"""
    print(msg)


def loadFileData():
    # 加载文件数据
    users = []
    with open(filePath, 'r', encoding='utf-8') as fileObj:
        for i in fileObj:
            line = i.strip('\n').split(',')
            # 将用户数据包装成一个字典
            users.append(dict(zip(tableField, line)))
    return users


def splitString(content, separatorCharacterName=None, numberOfSeparations=-1):
    """
    分隔字符串
    :param content: 需要分隔的字符串
    :param separatorCharacterName: 以什么字符来分隔
    :param numberOfSeparations: 分隔次数,默认分隔所有
    :return:
    """
    if separatorCharacterName:
        return content.split(separatorCharacterName, numberOfSeparations)
    else:
        return content.split()

def add(content):
    pass


def delete(content):
    pass


def update(content):
    pass


def select(content):
    pass


def main(sql):
    sqlCommand, sqlContent = splitString(sql, separatorCharacterName=' ', numberOfSeparations=1)
    action = sqlCommand.lower()
    commandType = {
        'add': add,
        'delete': delete,
        'update': update,
        'select': select
    }
    if action == 'add':
        commandType[action](sqlContent)
    elif action == 'delete':
        commandType[action](sqlContent)
    elif action == 'update':
        commandType[action](sqlContent)
    elif action == 'select':
        commandType[action](sqlContent)
    else:
        print('invalid error')


if __name__ == '__main__':
    # 程序的路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 表的名称
    tableName = 'staff_table.db'
    # 文件的存储目录
    rootPath = os.path.join(BASE_DIR, 'data')
    # 文件绝对路径
    filePath = os.path.join(rootPath, tableName)
    # 写入基础数据
    initializeBasicData()
    tableField = ['staff_id', 'name', 'age', 'phone', 'dept', 'enroll_date']
    while True:
        choice = input("mysql>  ")
        if choice.lower() == 'q':
            print('Bye Bye...')
            break
        elif choice.lower() == 'h' or choice.lower() == 'help':
            help()
        elif choice.lower() == 'show':
            # 查看当前数据人员名单
            users = [list(user.values()) for user in loadFileData()]
            # 形成数据框,并打印出来
            print(tabulate([tableField] + users))
            print('共计 %d 个人员' % len(users))
        else:
            main(choice)
