#!_*_coding:utf-8_*_
#__author__:"Alex Li"


import json
# acc_dic = {
#     'id': 1234,
#     'password': 'abc',
#     'credit': 15000,
#     'balance': 15000,
#     'enroll_date': '2016-01-02',
#     'expire_date': '2021-01-01',
#     'pay_day': 22,
#     'status': 0 # 0 = normal, 1 = locked, 2 = disabled
# }
acc_dic = {
    'id': 'cc',
    'password': 'abc',
    'credit': 15000,
    'balance': 15000,
    'enroll_date': '2016-01-02',
    'expire_date': '2021-01-01',
    'pay_day': 22,
    'status': 0 # 0 = normal, 1 = locked, 2 = disabled
}

#print(json.dumps(acc_dic))
with open(r'.\\accounts\\cc.json', 'w',encoding='utf-8') as f:
    json.dump(acc_dic, f)
