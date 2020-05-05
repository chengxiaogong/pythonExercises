# _*_ coding; utf-8 _*_
# author: cc
#


def loadFileData():
    # 加载文件数据
    users = []
    title = ['staff_id', 'name', 'age', 'phone', 'dept', 'enroll_date']
    filename = "./files/staff_table.txt"
    with open(filename, 'r', encoding='utf-8') as fileObj:
        for i in fileObj:
            line = i.strip('\n').split(',')
            users.append(dict(zip(title, line)))
    return users


def updateFileData(users):
    if users:
        f = open('./files/staff_table.txt', 'w', encoding='utf-8')
        for item in users:
            content = ','.join(list(item.values()))
            f.write(content + '\n')
        f.close()


def separate(*args):
    # 分隔字符串
    if len(args) == 2:
        content, seq = args
        return content.split(seq)
    elif len(args) == 1:
        content = args[0]
        # 以空格分隔字符串
        return content.split()


def splitExpression(string, seq):
    """
    拆分表达式
    :param string: 表达式字符串
    :param seq: 表达式符号
    :return:
    """
    ret = separate(string, seq)
    left = ret[0].replace(' ', '')
    right = ret[1]
    value = right.replace(' ', '').strip('"')
    return left, right, value


def filterData(condition, fileData):
    """
    过滤数据
    :param condition: 条件表达式, age >= 22
    :param fileData: 文件中的数据
    :return:
    """
    result = []
    if condition.count('>=') >= 1:
        seqName = '>='
        left, right, value = splitExpression(condition, seqName)
        result = [item for item in fileData if item[left] >= value]
    elif condition.count('<=') >= 1:
        seqName = '<='
        left, right, value = splitExpression(condition, seqName)
        result = [item for item in fileData if item[left] <= value]
    elif condition.count('=') >= 1:
        seqName = '='
        left, right, value = splitExpression(condition, seqName)
        result = [item for item in fileData if item[left] == value]
    elif condition.count('>') >= 1:
        seqName = '>'
        left, right, value = splitExpression(condition, seqName)
        result = [item for item in fileData if item[left] > value]
    elif condition.count('<') >= 1:
        seqName = '<'
        left, right, value = splitExpression(condition, seqName)
        result = [item for item in fileData if item[left] < value]
    elif condition.count('like') >= 1:
        seqName = 'like'
        left, right, value = splitExpression(condition, seqName)
        result = [item for item in fileData if value in item[left]]
    return result


def checkPhoneExists(phone, phone_list):
    """
    检查手机号是否已经存在
    :param phone:
    :param phone_list:
    :return:
    """
    result = [item['phone'] for item in phone_list]
    if phone in result:
        return True
    else:
        return False


def insert(sql, fileData):
    """
    插入数据
    可创建新员工纪录，以phone做唯一键(即不允许表里有手机号重复的情况)，staff_id需自增
    :param sql: SQL语句
    :param fileData: 文件中的数据
    :return:
    """
    name = ' '.join(sql.split(',')[0].split()[2:])
    age, phone, dept, enroll_date = sql.split(',')[1:]
    if checkPhoneExists(phone, fileData):
        print('phone %s exists' % phone)
    else:
        # staff_id 自增
        new_id = str(int(fileData[-1]['staff_id']) + 1)
        fileData.append(
            {
                'staff_id': new_id,
                'name': name,
                'age': age,
                'phone': phone,
                'dept': dept,
                'enroll_date': enroll_date
            }
        )
        return fileData


def delete(filterFunction, expression, fileData):
    """
    删除SQL
    :param filterFunction: 调用过滤函数
    :param expression: 查询表达式
    :param fileData: 文件中的数据
    :return:
    """
    data = filterFunction(expression, fileData)
    if len(data) == 0:
        print('data not exists.')
    else:
        userId = data[0]['staff_id']
        for k, v in enumerate(fileData):
            if v['staff_id'] == userId:
                print('user %s delete success' % fileData.pop(k))
        return fileData


def update(filterFunction, expression, fields, fileData):
    """
    修改SQL
    :param filterFunction: 调用过滤函数
    :param expression: 查询表达式
    :param fields: 需要修改的字段列表
    :param fileData: 文件中的数据
    :return:
    """
    dic = {}
    if ',' in fields[1]:
        for item in separate(fields[1], ','):
            result = separate(item, '=')
            name = result[0].strip(' ').strip('"')
            value = result[1].strip(' ').strip('"')
            dic[name] = value
    else:
        result = separate(fields[1], '=')
        name = result[0].strip(' ').strip('"')
        value = result[1].strip(' ').strip('"')
        dic[name] = value
    data = filterFunction(expression, fileData)
    users = [item['staff_id'] for item in data]
    for item in fileData:
        if item['staff_id'] in users:
            for key in dic:
                if item.get(key):
                    item[key] = dic[key]
    return fileData


def select(fieldString, filterFunction, expression, fileData):
    """
    查询SQL
    :param fieldString: 需要查询哪些字段
    :param filterFunction: 调用过滤函数
    :param expression: 查询表达式
    :param fileData: 文件中的数据
    :return:
    """
    data = filterFunction(expression, fileData)
    if fieldString == '*':
        for item in data:
            print(list(item.values()))
    else:
        # 只显示特定几个字段的查询结果
        field = fieldString.split(',')
        for item in data:
            for i in range(0, len(field)):
                print(item[field[i]], end=' ')
            print('')


def main(sql):
    seq = 'where' if sql.find('where') != -1 else 'WHERE'
    result = loadFileData()
    if sql.lower().startswith('find'):
        # 查询
        ret = separate(sql, seq)
        col = separate(ret[0])[1]
        condition = separate(ret[1], ',')
        select(col, filterData, condition[0], result)
    elif sql.lower().startswith('add'):
        # 插入
        updateFileData(insert(sql, result))
    elif sql.lower().startswith('del'):
        # 删除
        ret = separate(sql, seq)
        condition = separate(ret[1], ',')
        updateFileData(delete(filterData, condition[0], result))
    elif sql.lower().startswith('update'):
        # 修改
        ret = separate(sql, seq)
        condition = separate(ret[1], ',')
        seq2 = 'set' if sql.find('set') != -1 else 'SET'
        fields = separate(ret[0], seq2)
        updateFileData(update(filterData, condition[0], fields, result))
    else:
        print('invalid error')


if __name__ == '__main__':
    while True:
        sql_cmd = input("mysql>  ")
        if sql_cmd:
            if sql_cmd == "quit":
                print('Bye')
                break
            else:
                main(sql_cmd)
