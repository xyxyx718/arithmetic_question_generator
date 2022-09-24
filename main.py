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


def main():
    p = parameter_check(sys.argv)
    if p[0] == 1:
        n, r = p[1], p[2]

        text, ans_text = output(generate(n, r))
        write_file(text, 'Exercises.txt')
        write_file(ans_text, 'Answers.txt')

    elif p[0] == 2:
        e, a = p[1], p[2]

        exercises = read_file(e)
        answer = read_file(a)

        exercises = re.findall(
            r'\d+\. ([ 0-9\+−×÷’/\(\)]+)=[ \n$]+', exercises)
        answer = re.findall(r'\d+\. ([ 0-9’/]+)[ \n$]+', answer)

        Correct = []
        Wrong = []
        for i in range(len(exercises)):
            if calculate(exercises[i]) == calculate(answer[i]):
                Correct.append(i+1)
            else:
                Wrong.append(i+1)
        
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

        write_file(text, 'Grade.txt')

    else:
        print('Parameter Error')
        return -1

    return 0


if __name__ == '__main__':
    main()
