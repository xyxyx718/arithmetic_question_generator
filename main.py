# coding:utf-8

import re
import sys
from random import randint
from fractions import Fraction

from generater import generate


a = sys.argv

signs = ['+', '−', '×', '÷']


# 参数检查
def parameter_check(a):
    n=10
    if len(a)==3:
        if a[1]!='-r':
            return -1
        r=re.sub(r'\D', '', a[2])
        if r=='':
            return -1
        else:
            r=int(r)
    elif len(a)==5:
        if a[1]=='-n' and a[3]=='-r':
            n=re.sub(r'\D', '', a[2])
            r=re.sub(r'\D', '', a[4])
            if n=='' or r=='':
                return -1
            else:
                n=int(n)
                r=int(r)
        elif a[1]=='-r' and a[3]=='-n':
            n=re.sub(r'\D', '', a[4])
            r=re.sub(r'\D', '', a[2])
            if n=='' or r=='':
                return -1
            else:
                n=int(n)
                r=int(r)
        else:
            return -1
    return n,r







def output(l: list):
    text = ''
    for i in range(1, l[0][0]+1):  # n
        text = text+'%d. ' % i  # 序号
        text = text+l[i][10]  # 题目
        text = text + ' = \n'  # 等号和换行

    return text



def main(a):
    print(a)


if __name__ == '__main__':
    n = 10
    r = 10

    list_0 = generate(n, r)
    print(output(list_0))
