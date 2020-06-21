# -*- coding: utf-8 -*-
# 


"""
数据库连接引擎
"""

import os
import json
from conf import settings


def file_db_handle(conn_param):
    """
    文件句柄
    :param conn_param:
    :return:
    """
    print('database file: ', conn_param)
    return file_execute


def db_handler():
    conn_param = settings.DATABASE
    if conn_param['engine'] == 'file_storage':
        return file_db_handle(conn_param)
    elif conn_param['engine'] == 'mysql':
        pass  # todo


def file_execute(sql, **kwargs):
    """
    查询sql语句
    select * from accounts where account=cc
    update accounts where account=1234
    :param sql:
    :param kwargs:
    :return:
    """
    print(sql, kwargs)
    conn_param = settings.DATABASE
    db_path = '/'.join([conn_param['path'], conn_param['name']])
    print('db_path: ', db_path)
    sql_list = sql.split('where')
    if sql_list[0].strip().startswith('select') and len(sql_list) > 1:
        print('查询')
        col, val = sql_list[1].strip().split('=')
        if col == 'account':
            account_file = '%s/%s.json' % (db_path, val)
            if os.path.isfile(account_file):
                with open(account_file, 'r') as fileObj:
                    data = json.load(fileObj)
                    return data
            else:
                exit('%s user db file not exists' % account_file)
    elif sql_list[0].strip().startswith('update') and len(sql_list) > 1:
        print('修改')
        col, val = sql_list[1].strip().split('=')
        if col == 'account':
            account_file = '%s/%s.json' % (db_path, val)
            if os.path.isfile(account_file):
                access_data = kwargs.get('account_data')
                with open(account_file, 'w') as fileObj:
                    json.dump(access_data, fileObj)
                return True
            else:
                exit('%s user db file not exists' % account_file)
