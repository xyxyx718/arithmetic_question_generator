# coding:utf-8

import re
import sys
from random import randint
from fractions import Fraction

a = sys.argv

signs = ['+', '−', '×', '÷']

lenght = len(a)

if lenght == 1:
    print("No arguments passed")
elif lenght == 3:
    if a[1] == '-n':
        n = int(a[2])  # 记得加报错限制范围
    elif a[1] == '-r':
        r = int(a[2])
    else:
        print("Invalid arguments")
elif lenght == 5:
    if a[1] == '-n' and a[3] == '-r':
        n = int(a[2])
        r = int(a[4])
    elif a[1] == '-r' and a[3] == '-n':
        n = int(a[4])
        r = int(a[2])
    else:
        print("Invalid arguments")
else:
    print("Invalid arguments")


# 运算符数量（0），括号位置（1~2），运算符是什么（3~5），运算数（6~9），字符串（10），空的补零
def generate(n, r, l: list):
    for i in range(n):
        # 空列表
        small_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '']

        # 运算符数量
        signs_num = randint(1, 3)
        small_list[0] = signs_num

        # 生成括号位置
        # 0 无括号
        if signs_num > 1:
            roll = randint(0, 1)
            if roll == 1:  # roll为1时有括号
                small_list[1] = randint(1, signs_num)
                if small_list[1] != 1: # 如果左括号在最左边，右括号就不能在最右边
                    small_list[2] = randint(small_list[1]+2, signs_num+2)
                else:
                    small_list[2] = randint(small_list[1]+2, signs_num+1)

        # 生成运算符
        for j in range(3, 3+signs_num):
            small_list[j] = randint(0, 3)

        # 生成运算数
        for j in range(6, 6+signs_num+1):
            if j > 0 and small_list[j-4] == 3:
                small_list[j] = randint(1, r)
            else:
                small_list[j] = randint(0, r)
        l.append(small_list)

    return l


def output(l: list):
    text = ''
    for i in range(1,l[0][0]+1): # n
        text = text+'%d. ' % (i+1) # 序号

        if l[i][1] == 0: # 无括号
            text = text + '%d' %l[i][6]
            for j in range(l[i][0]):
                text = text + ' %s %d' %(signs[l[i][j+3]], l[i][j+7])

        else: # 有括号
            kuohao = 1 # 1左括号 2右括号
            if l[i][1] == 1:
                text = text + '('
                kuohao = 2
            text = text + '%d' %l[i][6]
            for j in range(l[i][0]):
                if kuohao == 2 and j+2 == l[i][2]:  # 右括号
                    text = text + ')'
                    kuohao = 3
                text = text + ' %s ' %(signs[l[i][j+3]]) # 运算符
                if kuohao == 1 and j+2 == l[i][1]: # 左括号
                    text = text + '('
                    kuohao = 2
                text = text + '%d' %(l[i][j+7]) # 运算数
            if kuohao == 2: # 右括号
                text = text + ')'
        text = text + ' = \n' # 等号和换行

    return text
'''
        if l[i][0]==1:
            text = text+'%d %s %d = ' % (l[i][6], signs[l[i][3]], l[i][7])
        elif l[i][0]==2:
            if 
            text = text+'%d %s %d %s %d = ' % (l[i][6], signs[l[i][3]], l[i][7], signs[l[i][4]], l[i][8])
'''
def main(a):
    print(a)


if __name__ == '__main__':
    n = 100
    r = 10
    list_0 = []
    list_0.append([n, r])
    list_1 = generate(n, r, list_0)
    print(output(list_1))
