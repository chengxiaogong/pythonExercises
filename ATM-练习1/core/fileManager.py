# _*_ coding; utf-8 _*_
# author: cc
#

import json


def loadFileData(filePath):
    # 加载文件中的数据
    with open(filePath, 'r') as fileObj:
        return json.load(fileObj)


def updateFileDate(filePath, content):
    """
    修改文件中的数据
    :param filePath: 文件名
    :param content: 内容
    :return:
    """
    with open(filePath, 'w') as fileObj:
        return json.dump(content, fileObj)

