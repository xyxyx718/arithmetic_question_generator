# coding:utf-8

import sys
from fractions import Fraction

from generater import generate
from re_calculater import *
from readandwrite import *

signs = ['+', '−', '×', '÷']


def parameter_check(a):
    # 参数检查
    # l[0] 1→nr 2→ea -1→error
    n = 10  # 题目数量 默认10
    # 2个参数
    if len(a) == 3:
        if a[1] != '-r':
            return [-1]
        elif re.search(r'\D', a[2]) is not None:
            return [-1]
        r = int(a[2])
        return [1, n, r]
    # 4个参数
    elif len(a) == 5:
        if (a[1] == '-n') and (a[3] == '-r'):
            if re.search(r'\D', a[2] + a[4]) is not None:
                return [-1]
            n = int(a[2])
            r = int(a[4])
            return [1, n, r]
        elif (a[1] == '-r') and (a[3] == '-n'):
            if re.search(r'\D', a[2] + a[4]) is not None:
                return [-1]
            r = int(a[2])
            n = int(a[4])
            return [1, n, r]
        elif (a[1] == '-e') and (a[3] == '-a'):
            if re.match(r'.*\.txt$', a[2], flags=0) is not None:
                e = a[2]
            else:
                return [-1]
            if re.match(r'.*\.txt$', a[4], flags=0) is not None:
                a = a[4]
            else:
                return [-1]
            return [2, e, a]
        else:
            return [-1]
    else:
        return [-1]


def main(a):
    # 错误代码
    # -1 参数错误
    # -2 文件编码错误或不存在
    # -3 Grade.txt文件无法写入
    # -4 题目数量与答案数量不符
    # -5 所给题目存在除以0错误

    p = parameter_check(a)
    if p[0] == 1:
        # 生成题目
        n, r = p[1], p[2]

        text, ans_text = output_format(generate(n, r))
        write_file(text, 'Exercises.txt')
        write_file(ans_text, 'Answers.txt')

        print('生成题目成功！')
        print('题目已保存至Exercises.txt')
        print('答案已保存至Answers.txt')

    elif p[0] == 2:
        # 检查答案
        e, a = p[1], p[2]

        # 读取文件
        exercises = read_file(e)
        answers = read_file(a)
        if (exercises == -1) or (answers == -1):
            print('文件编码错误或不存在')
            return -2

        # 格式化
        exercises = input_format(exercises, 'e')
        answers = input_format(answers, 'a')

        # 判断正误
        if len(exercises) != len(answers):
            print('题目数量与答案数量不符')
            return -4

        correct = []
        wrong = []
        for i in range(len(exercises)):
            ee = re_calculate(exercises[i])
            aa = Fraction(answers[i])
            if ee is None:
                print('第%d题除以0或出现负数，题目有误' % (i + 1))
                return -5
            if ee == aa:
                correct.append(i + 1)
            else:
                wrong.append(i + 1)

        # 生成文本
        text = 'Correct: %d' % len(correct)
        for i in range(len(correct)):
            if i == 0:
                text = text + ' ('
            text = text + '%d' % correct[i]
            if i != len(correct) - 1:
                text = text + ', '
            else:
                text = text + ')'

        text = text + '\nWrong: %d' % len(wrong)
        for i in range(len(wrong)):
            if i == 0:
                text = text + ' ('
            text = text + '%d' % wrong[i]
            if i != len(wrong) - 1:
                text = text + ', '
            else:
                text = text + ')'

        # 写入文件
        if write_file(text, 'Grade.txt') < 0:
            print('Grade.txt文件无法写入！')
            return -3  # Grade.txt文件无法写入
        print('结果已成功写入到Grade.txt文件！')

    else:
        print('参数错误!')
        print('正确格式：%s -n a -r b' % a[0])
        print('其中a为题目数量，b为题目中数值的范围')
        print('或：%s -e a.txt -a b.txt' % a[0])
        print('其中a.txt为题目文件，b.txt为答案文件')
        return -1  # 参数错误

    return 0


if __name__ == '__main__':
    main(sys.argv)
