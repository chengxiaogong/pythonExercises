# -*- coding: utf-8 -*-

"""
@author: cc
@time: 2020/5/21 14:45
"""

import os


print(os.path.abspath(__file__))
print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))