# coding:utf-8

import re
import sys
from random import randint
from fractions import Fraction

from generater import generate
from calculater import calculate
from readandwrite import *


signs = ['+', '−', '×', '÷']


# 参数检查
# l[0] 1→nr 2→ea -1→error
def parameter_check(a):
    n = 10  # 题目数量 默认10
    if len(a) == 3:
        if a[1] != '-r':
            l = [-1]
        elif re.search(r'\D', a[2]) != None:
            l = [-1]
        r = int(a[2])
        l = [1, n, r]
    elif len(a) == 5:
        if (a[1] == '-n') and (a[3] == '-r'):
            if re.search(r'\D', a[2]+a[4]) != None:
                l = [-1]
            n = int(a[2])
            r = int(a[4])
            l = [1, n, r]
        elif (a[1] == '-r') and (a[3] == '-n'):
            if re.search(r'\D', a[2]+a[4]) != None:
                l = [-1]
            r = int(a[2])
            n = int(a[4])
            l = [1, n, r]
        elif (a[1] == '-e') and (a[3] == '-a'):
            if re.match(r'.*\.txt$', a[2], flags=0) != None:
                e = a[2]
            if re.match(r'.*\.txt$', a[4], flags=0) != None:
                a = a[4]
            l = [2, e, a]
        else:
            l = [-1]
    else:
        l = [-1]
    return l

# 错误代码
# -1 参数错误
# -2 文件编码错误或不存在
# -3 Grade.txt文件无法写入
# -4 题目数量与答案数量不符
# -5 所给题目存在除以0错误


def main(p):
    p = parameter_check(p)
    if p[0] == 1:
        # 生成题目
        n, r = p[1], p[2]

        text, ans_text = output(generate(n, r))
        write_file(text, 'Exercises.txt')
        write_file(ans_text, 'Answers.txt')

    elif p[0] == 2:
        # 检查答案
        e, a = p[1], p[2]

        # 读取文件
        exercises = read_file(e)
        answer = read_file(a)
        if (exercises == -1) or (answer == -1):
            print('文件编码错误或不存在')
            return -2

        # 格式化
        exercises = re.findall(
            r'\d+\. ([ 0-9\+−×÷’/\(\)]+)=[ \n$]+', exercises)
        answer = re.findall(r'\d+\. ([ 0-9’/]+)[ \n$]+', answer)

        # 判断正误
        if (len(exercises) != len(answer)):
            print('题目数量与答案数量不符')
            return -4

        Correct = []
        Wrong = []
        for i in range(len(exercises)):
            ee = calculate(exercises[i])
            aa = calculate(answer[i])
            if ee < 0:
                print('第%d题除以0，题目有误' % (i+1))
                return -5
            if ee == aa:
                Correct.append(i+1)
            else:
                Wrong.append(i+1)
        # 生成文本
        text = 'Correct: %d' % len(Correct)
        for i in range(len(Correct)):
            if i == 0:
                text = text+' ('
            text = text+'%d' % Correct[i]
            if i != len(Correct)-1:
                text = text+', '
            else:
                text = text+')'
        text = text+'\nWrong: %d' % len(Wrong)
        for i in range(len(Wrong)):
            if i == 0:
                text = text+' ('
            text = text+'%d' % Wrong[i]
            if i != len(Wrong)-1:
                text = text+', '
            else:
                text = text+')'

        # 写入文件
        if write_file(text, 'Grade.txt') < 0:
            print('Grade.txt文件无法写入')
            return -3  # Grade.txt文件无法写入

    else:
        print('参数错误!')
        print('正确格式：Myapp.exe -n a -r b')
        print('其中a为题目数量，b为题目中数值的范围')
        print('或：Myapp.exe -e a.txt -a b.txt')
        print('其中a.txt为题目文件，b.txt为答案文件')
        return -1  # 参数错误

    return 0


if __name__ == '__main__':
    main(sys.argv)
