#!_*_coding:utf-8_*_
# __author__:"Alex Li"

"""
handle all the database interactions
"""

import json, os
from conf import settings


def file_db_handle(conn_params):
    """
    parse the db file path
    :param conn_params: the db connection params set in settings
    :return:
    """
    print('file db:', conn_params)
    return file_execute  # 返回文件执行方法的内存地址


def db_handler():
    """
    connect to db
    :return:a
    """
    # DATABASE = {'engine': 'file_storage', 'name':'accounts','path': "D:\\projects\\py3_training\\atm\\atm\\db"}
    conn_params = settings.DATABASE
    if conn_params['engine'] == 'file_storage':
        return file_db_handle(conn_params)
    elif conn_params['engine'] == 'mysql':
        pass  # todo


# update accounts where account=1234, 文件中的用户数据
def file_execute(sql, **kwargs):  # select * from accounts where account=cc
    # DATABASE = {'engine': 'file_storage', 'name':'accounts','path': "D:\\projects\\py3_training\\atm\\atm\\db"}
    conn_params = settings.DATABASE
    # D:\\projects\\py3_training\\atm\\atm\\db\\accounts
    db_path = '%s/%s' % (conn_params['path'], conn_params['name'])
    print(sql, db_path)
    sql_list = sql.split("where")  # ['select * from accounts ', ' account=cc']
    print(sql_list)
    if sql_list[0].startswith("select") and len(sql_list) > 1:  # has where clause
        # 查询用户数据
        column, val = sql_list[1].strip().split("=")  # ['account', 'cc']
        if column == 'account':
            # 拼接用户数据存放文件
            account_file = "%s/%s.json" % (db_path, val)
            print(account_file)  # D:\\projects\\py3_training\\atm\\atm\\db\\accounts\\cc.json
            if os.path.isfile(account_file):
                with open(account_file, 'r') as f:
                    account_data = json.load(f)  # 加载用户文件中的数据
                    return account_data
            else:
                exit("\033[31;1mAccount [%s] does not exist!\033[0m" % val)
    elif sql_list[0].startswith("update") and len(sql_list) > 1:  # has where clause
        # 更新用户数据
        column, val = sql_list[1].strip().split("=")
        if column == 'account':
            account_file = "%s/%s.json" % (db_path, val)
            if os.path.isfile(account_file):
                account_data = kwargs.get("account_data")
                with open(account_file, 'w') as f:
                    json.dump(account_data, f)
                return True
