# -*- coding: utf-8 -*-
# 

import os
import sys
import json

acc_dic = {
    'id': 'cc',
    'password': 'abc',
    'credit': 15000,
    'balance': 15000,
    'enroll_date': '2016-01-02',
    'expire_date': '2021-01-01',
    'pay_day': 22,
    'status': 0  # 0 = normal, 1 = locked, 2 = disabled
}


# 生成一个初始的账户数据 ,把这个数据存成一个 以这个账户id为文件名的文件,放在accounts目录 就行了,程序自己去会这里找
db_path = os.path.join(sys.path[0], "accounts")
with open("%s/%s.json" % (db_path, "cc"), "w") as fileObj:
    json.dump(acc_dic, fileObj)
