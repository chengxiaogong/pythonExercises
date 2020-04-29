# _*_ coding; utf-8 _*_
# author: cc
#


def loadFileData():
    # 加载文件数据
    users = []
    title = ['staff_id', 'name', 'age', 'phone', 'dept', 'enroll_date']
    filename = "./files/staff_data.txt"
    with open(filename, 'r', encoding='utf-8') as fileObj:
        for i in fileObj:
            line = i.strip('\n').split(',')
            users.append(dict(zip(title, line)))
    return users


def updateFileData(users):
    if users:
        f = open('./files/staff_data.txt', 'w', encoding='utf-8')
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
    # 拆分表达式
    ret = separate(string, seq)
    left = ret[0].replace(' ', '')
    right = ret[1]
    return left, right


def select(condition, col, fileData):
    """
    查询SQL
    :param condition: 条件表达式, age >= 22
    :param col: 需要查询哪些字段
    :param fileData: 文件中的数据
    :return:
    """
    if condition.count('>=') >= 1:
        seqName = '>='
        left, right = splitExpression(condition, seqName)
        value = right.replace(' ', '').strip('"')
        if col == '*':
            for item in fileData:
                if item[left] >= value:
                    print(list(item.values()))
        else:
            field_list = col.split(',')
            for item in fileData:
                if item[left] >= value:
                    for i in range(0, len(field_list)):
                        print(item[field_list[i]], end=' ')
                    print('')
    elif condition.count('<=') >= 1:
        seqName = '<='
        left, right = splitExpression(condition, seqName)
        value = right.replace(' ', '').strip('"')
        if col == '*':
            for item in fileData:
                if item[left] <= value:
                    print(list(item.values()))
        else:
            field_list = col.split(',')
            for item in fileData:
                if item[left] <= value:
                    for i in range(0, len(field_list)):
                        print(item[field_list[i]], end=' ')
                    print('')
    elif condition.count('=') >= 1:
        seqName = '='
        left, right = splitExpression(condition, seqName)
        value = right.replace(' ', '').strip('"')
        if col == '*':
            for item in fileData:
                if item[left] == value:
                    print(list(item.values()))
        else:
            field_list = col.split(',')
            for item in fileData:
                if item[left] == value:
                    for i in range(0, len(field_list)):
                        print(item[field_list[i]], end=' ')
                    print('')
    elif condition.count('>') >= 1:
        seqName = '>'
        left, right = splitExpression(condition, seqName)
        value = right.replace(' ', '').strip('"')
        if col == '*':
            for item in fileData:
                if item[left] > value:
                    print(list(item.values()))
        else:
            field_list = col.split(',')
            for item in fileData:
                if item[left] > value:
                    for i in range(0, len(field_list)):
                        print(item[field_list[i]], end=' ')
                    print('')
    elif condition.count('<') >= 1:
        seqName = '<'
        left, right = splitExpression(condition, seqName)
        value = right.replace(' ', '').strip('"')
        if col == '*':
            for item in fileData:
                if item[left] < value:
                    print(list(item.values()))
        else:
            field_list = col.split(',')
            for item in fileData:
                if item[left] < value:
                    for i in range(0, len(field_list)):
                        print(item[field_list[i]], end=' ')
                    print('')
    elif condition.count('like') >= 1:
        seqName = 'like'
        left, right = splitExpression(condition, seqName)
        value = right.replace(' ', '').strip('"')
        if col == '*':
            for item in fileData:
                if value in item[left]:
                    print(list(item.values()))
        else:
            field_list = col.split(',')
            for item in fileData:
                if value in item[left]:
                    for i in range(0, len(field_list)):
                        print(item[field_list[i]], end=' ')
                    print('')

def checkPhoneExists(phone, phone_list):
    """
    检查手机号是否已经存在
    :param phone:
    :param phone_list:
    :return:
    """
    result = [ item['phone'] for item in phone_list]
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
    result = loadFileData()
    name = ' '.join(sql.split(',')[0].split()[2:])
    age, phone, dept, enroll_date = sql.split(',')[1:]
    if checkPhoneExists(phone, fileData):
        print('phone %s exists' % phone)
    else:
        new_id = str(int(result[-1]['staff_id']) + 1)
        result.append(
            {
                'staff_id': new_id,
                'name': name,
                'age': age,
                'phone': phone,
                'dept': dept,
                'enroll_date': enroll_date
            }
        )
        return result


def main(sql):
    result = loadFileData()
    if sql.startswith('find'):
        seq = 'where' if sql.find('where') != -1 else 'WHERE'
        ret = separate(sql, seq)
        col = separate(ret[0])[1]
        condition = separate(ret[1], ',')
        print('col: ', col)
        select(condition[0], col, result)
    elif sql.startswith('add'):
        updateFileData(insert(sql, result))
    elif sql.startswith('del'):
        print('删除')
    elif sql.startswith('update'):
        print('修改')
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
