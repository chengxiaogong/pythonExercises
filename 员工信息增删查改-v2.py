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
import re
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
    语法: del from staff_tables where  staff_id=3
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


def storageData(users):
    """
    存储数据
    :param users: 将修改后的数据重新写到文件中
    :return:
    """
    if users:
        f = open(filePath, 'w', encoding='utf-8')
        for item in users:
            content = ','.join(list(item.values()))
            f.write(content + '\n')
        f.close()


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


def filterFunction(fieldKey, fieldValue, symbol, users):
    """
    过滤器函数
    :param fieldKey: 字段名称
    :param fieldValue: 字段值
    :param symbol: 符号
    :param users: 用户数据
    :return list:
    """
    fieldKey, fieldValue = fieldKey.strip(), fieldValue.strip('"')  # 初始化变量
    if fieldKey not in tableField:
        print('table field |%s| not exists' % fieldKey)
        return []
    else:
        # fieldValue = fieldValue.strip('"')
        field_symbol_compare = {
            ">": [item for item in users if item[fieldKey] > fieldValue],
            "<": [item for item in users if item[fieldKey] < fieldValue],
            "=": [item for item in users if item[fieldKey] == fieldValue],
            ">=": [item for item in users if item[fieldKey] >= fieldValue],
            "<=": [item for item in users if item[fieldKey] <= fieldValue],
            "like": [item for item in users if fieldValue in item[fieldKey]],
        }
        return field_symbol_compare.get(symbol)


def checkPhoneExists(phone, users):
    """
    检查手机号是否已经存在
    :param phone: 用户输入的手机号
    :param users: 表中的用户数据
    :return bool: False 表示手机号已经存在, True 表示手机号不存在
    """
    num, checkStatus = len(phone), True  # 初始化变量状态
    if num != 11:
        print('%s Illegal mobile number !!!' % phone)
        checkStatus = False
    else:
        # 效验手机号是否已经存在
        result = [item['phone'] for item in users]
        if phone in result:
            print('%s phone exists' % phone)
            checkStatus = False
    return checkStatus


def checkTableExists(tableName):
    """
    效验表是否存在
    :param tableName: 表的名称
    :return bool:
    """
    if not os.path.exists('%s.db' % os.path.join(rootPath, tableName)):
        print('%s table not exists.' % tableName)
        return False
    else:
        return True


def deleteEmptyElement(content):
    """
    删除列表中的空元素
    :param content: 内容
    :return:
    """
    while '' in content:
        content.remove('')
    return content


def add(content):
    """
    新增用户数据
    :param content: 内容
    :return:
    """
    users = loadFileData()
    table, content = splitString(content, separatorCharacterName=' ', numberOfSeparations=1)
    if checkTableExists(table):
        data = splitString(content, separatorCharacterName=',')
        if len(data) + 1 == len(users[0]):
            phone = data[2]
            # 效验手机号是否已经存在
            if checkPhoneExists(phone, users):
                # 用户ID 自增
                staffId = str(len(users) + 1)
                data.insert(0, staffId)
                sqlContent = dict(zip(tableField, data))
                users.append(sqlContent)
                return storageData(users)
        else:
            print('sql error')


def delete(content):
    """
    删除用户数据
    :param content: 内容
    :return:
    """
    fieldKey, fieldValue, symbol, count = None, None, None, 0  # 初始化变量
    users = loadFileData()
    result = splitString(content, separatorCharacterName=' ')
    content = deleteEmptyElement(result)
    if content[0].lower() == 'from' and content[2] in ['where', 'WHERE']:
        symbolValue = 'WHERE' if content.count('WHERE') == 1 else 'where'
        condition = content[content.index(symbolValue)+1:]  # ['from', 'staff_tables', 'where', 'staff_id=3']
        if len(condition) == 1:
            pattern = '(?P<fieldKey>\w.*)(?P<symbol>\>|<|=|<=|\>=|like)(?P<fieldValue>\w.*)'
            matchingObject = re.search(pattern, condition[0])  # staff_id=3
            if matchingObject:
                fieldKey = matchingObject['fieldKey']
                symbol = matchingObject['symbol']
                fieldValue = matchingObject['fieldValue']
            else:
                print('matching condition error')
        elif len(condition) == 3:
            fieldKey, symbol, fieldValue = condition
        else:
            print('sql syntax error')
    else:
        print('sql syntax error')

    if fieldKey and fieldValue and symbol:
        data = filterFunction(fieldKey, fieldValue, symbol, users)
        if len(data) != 0:
            for k, v in enumerate(users):
                for j in data:
                    deleteUserId = j['staff_id']
                    userId = v['staff_id']
                    if userId == deleteUserId:
                        print('delete %s user ' % v['name'])
                        del users[k]
                        count += 1
        print('删除的用户数: %d' % count)
        return storageData(users)


def update(content):
    """
    更新数据
    :param content: 内容
    :return:
    """
    count, dic = 0, {}  # 初始化变量
    users = loadFileData()
    searchSet = 'SET' if content.count('SET') == 1 else 'set'
    searchWhere = 'WHERE' if content.count('WHERE') == 1 else 'where'
    split1 = splitString(content, searchSet)  # ['staff_table ', ' age = 25 WHERE  name = "Alex Li"']
    split2 = deleteEmptyElement(splitString(split1[1], separatorCharacterName=' '))  # ' age = 25 WHERE  name = "Alex Li"'
    split3 = splitString(' '.join(split2), separatorCharacterName=searchWhere)  # age = 25 WHERE  name = "Alex Li"
    field, condition = split3
    pattern = '\s*(?P<fieldKey>\w.*)\s*(?P<symbol>\>|<|=|<=|\>=|like)\s*"?(?P<fieldValue>\w.*)"?.*'
    # 匹配条件等式
    matchingObject = re.search(pattern, condition)  # age < 22 | name = "Alex Li"
    if matchingObject:
        fieldKey = matchingObject['fieldKey']
        symbol = matchingObject['symbol']
        fieldValue = matchingObject['fieldValue']
        # 筛选数据
        data = filterFunction(fieldKey, fieldValue, symbol, users)
        # 解析需要更改的字段和值
        if ',' in field:
            field_list = splitString(field, separatorCharacterName=',')
            for item in field_list:
                fieldKey, fieldValue = splitString(item, '=')
                dic[fieldKey.strip()] = fieldValue.strip().strip('"')
        else:
            fieldKey, fieldValue = splitString(field, '=')
            dic[fieldKey.strip()] = fieldValue.strip().strip('"')
        # 更新数据
        if len(dic) != 0:
            userId = [item['staff_id'] for item in data ]
            for item in users:
                if item['staff_id'] in userId:
                    for key in dic:
                        if item.get(key):
                            old = item.get(key)
                            new = dic[key]
                            if old != new:
                                item[key] = str(new)
                                count += 1
            print('更新受影响的条数: %d' % count)
            return storageData(users)
    else:
        print('matching condition error')


def select(content):
    """
    查询
    :param content: 内容
    :return:
    """
    users = loadFileData()
    result = splitString(content, separatorCharacterName=' ')
    if len(result) == 7 and result[1].lower() == 'from' and result[3].lower() == 'where':
        columnName, tableName, fieldKey, fieldValue = result[::2]
        if checkTableExists(tableName):
            data = filterFunction(fieldKey, fieldValue, result[5], users)
            count = 0  # 计数器
            if columnName == '*':
                for item in data:
                    print(item)
                    count += 1
            else:
                field_list = splitString(columnName, separatorCharacterName=',')
                # 筛选出不存在的字段
                col = [ item for item in field_list if item in tableField]
                for item in data:
                    for field in col:
                        print(item[field], end=' ')
                    print()
                    count += 1
            print('查询出来的条数: %d' % count)
    else:
        print('sql error')


def main(sql):
    sqlCommand, sqlContent = splitString(sql, separatorCharacterName=' ', numberOfSeparations=1)
    action = sqlCommand.lower()
    commandType = {
        'add': add,
        'del': delete,
        'update': update,
        'find': select
    }
    if action == 'add':
        commandType[action](sqlContent)
    elif action == 'del':
        commandType[action](sqlContent)
    elif action == 'update':
        commandType[action](sqlContent)
    elif action == 'find':
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
        elif choice:
            main(choice)
