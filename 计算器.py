# _*_ coding; utf-8 _*_
# author: cc
#

"""
需求
1 - 2 * ( (60-30 +(-40/5)*(9-2*5/3 + 7 /3*99/4*2998 +10*568/14 )) - (-4*3)/ (16-3*2) )等类似公式后
必须自己解析里面(),+,-,*,/符号和公式(不能调用eval等类似功能偷懒实现)，
运算后得出结果，结果必须与真实的计算器所得出的结果一致

匹配乘法: re.search('\d+\.?\d*[+-]?\*[+-]?\d+\.?\d*', s)
匹配除法: re.search('\d+\.?\d*[+-]?/[+-]?\d+\.?\d*', s)
匹配乘除法: re.search('\d+\.?\d*[+-]?[*/][+-]?\d+\.?\d*', s)
匹配加减法: re.search('[+-]?\d+\.?\d*[+-]\d+\.?\d*', s) # 注意这里应考虑等式最前面就有一个正或负号的情况
匹配括号: re.search('\([^()]*\)', s)
"""

import re


def formattingString(string):
    # 格式化字符串,这里做了一个递归处理
    if string.find(' ') >= 1:
        string = string.replace(' ', '')
        return formattingString(string)
    elif string.find('+-') >= 1:
        string = string.replace('+-', '-')
        return formattingString(string)
    elif string.find('--') >= 1:
        string = string.replace('--', '+')
        return formattingString(string)
    elif string.find('++') >= 1:
        string = string.replace('++', '+')
        return formattingString(string)
    elif string.find('-+') >= 1:
        string = string.replace('-+', '-')
        return formattingString(string)
    elif string.find('÷') >= 1:
        string = string.replace('÷', '/')
        return formattingString(string)
    elif string.find('×') >= 1:
        string = string.replace('×', '*')
        return formattingString(string)
    elif string.find('**') >= 1:
        string = string.replace('**', '*')
        return formattingString(string)
    return string


def checkExpression(string):
    # 效验字符串的合法性
    checkStatus = True
    if len(re.findall('[a-zA-z]', string)) != 0:
        # 表达式中含有大小字母
        print("expression invalid!!!")
        checkStatus = False
    if string.count('(') != string.count(')'):
        # 表达式中的左括号和右括号不匹配
        print("expression invalid!!!")
        checkStatus = False
    return checkStatus


def calcMulDiv(string):
    # 计算乘除法
    pattern = '\d+\.?\d*[+-]?[*/][+-]?\d+\.?\d*'
    while len(re.findall(pattern, string)) > 0:
        # 匹配表达式中的乘除法
        matchObject = re.search(pattern, string)
        if matchObject:
            # 获取匹配到的对象
            matchResult = matchObject.group()
            if '*' in matchResult:
                x, y = matchResult.split('*')
                # 计算乘法
                calcResult = str(float(x) * float(y))
                # 将计算后的结果替换掉原有匹配到的表达式
                string = formattingString(string.replace(matchResult, calcResult))
            elif '/' in matchResult:
                x, y = matchResult.split('/')
                # 计算除法
                calcResult = str(float(x) / float(y))
                # 将计算后的结果替换掉原有匹配到的表达式
                string = formattingString(string.replace(matchResult, calcResult))
    return string


def calcAddSub(string):
    # 计算加减法
    pattern = '[+-]?\d+\.?\d*[+-]\d+\.?\d*'
    while len(re.findall(pattern, string)) > 0:
        # 匹配表达式中的加减法
        matchObject = re.search(pattern, string)
        if matchObject:
            # 获取匹配到的对象
            matchResult = matchObject.group()
            if '+' in matchResult:
                x, y = matchResult.split('+')
                # 计算加法
                calcResult = str(float(x) + float(y))
                # 将计算后的结果替换掉原有匹配到的表达式
                string = formattingString(string.replace(matchResult, calcResult))
            elif '-' in matchResult:
                if len(re.findall('-', matchResult)) == 1:
                    x, y = matchResult.split('-')
                    # 计算减法
                    calcResult = str(float(x) - float(y))
                    # 将计算后的结果替换掉原有匹配到的表达式
                    string = formattingString(string.replace(matchResult, calcResult))
                elif len(re.findall('-', matchResult)) == 2:
                    # 这里判断表达式可能会出现2个负号的情况,那么这里我们就需要改变运算方式为加法,而不是减法
                    x, y = matchResult.split('-')[1:]
                    # 计算加法
                    calcResult = str(float(x) + float(y))
                    # 将计算后的结果替换掉原有匹配到的表达式
                    string = formattingString(string.replace(matchResult, '-' + calcResult))
    return string


def main(string):
    pattern = '\([^()]*\)'
    while string.count('(') > 0:
        # 计算括号内的内容
        matchObject = re.search(pattern, string)
        if matchObject:
            # 计算乘除法
            mulDivResults = formattingString(calcMulDiv(matchObject.group()))
            # 计算加减法
            addSubResults = formattingString(calcAddSub(mulDivResults))
            # 针对计算出来后的结果进行切片处理,如(-40/5) 计算出来后的结果就是(-8.0)
            string = string.replace(matchObject.group(), addSubResults[1:-1])
    else:
        # 计算括号外的内容
        # 计算乘除法
        mulDivResults = formattingString(calcMulDiv(string))
        # 计算加减法
        addSubResults = formattingString(calcAddSub(mulDivResults))
        string = string.replace(string, addSubResults)
    return string


if __name__ == '__main__':
    while True:
        source = input("输入需要计算的题: ")
        if not source:
            print("输入为空!!!")
            continue
        elif source == "q":
            print("bye bye...")
            break
        # 格式化字符串
        stringExpression = formattingString(source)
        # 效验表达式的合法性
        if checkExpression(stringExpression):
            print("您需要计算的表达式: ", stringExpression)
            print("我要开始计算了,请您稍等...")
            result = main(stringExpression)
            print("使用eval的计算结果: ", eval(stringExpression))
            print("使用计算器的计算结果: ", result)
            print("分隔线".center(150, '*'))
