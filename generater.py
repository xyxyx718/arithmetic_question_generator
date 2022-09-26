from cgi import print_arguments
from random import randint
from fractions import Fraction
from re_calculater import *
from transformer import transform
import re


def generate_loop(r):
# 生成一个small_list的前10个元素
# 即运算符数量（0），括号位置（1~2），运算符（3~5），运算数（6~9）
    # 空列表
    small_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # 运算符数量
    signs_num = randint(1, 3)
    small_list[0] = signs_num

    # 生成括号位置
    # 0 无括号
    if signs_num > 1:
        roll = randint(0, 1)
        if roll == 1:  # roll为1时有括号
            small_list[1] = randint(1, signs_num)
            if small_list[1] != 1:  # 如果左括号在最左边，右括号就不能在最右边
                small_list[2] = randint(small_list[1]+2, signs_num+2)
            else:
                small_list[2] = randint(small_list[1]+2, signs_num+1)

    # 生成运算符
    for j in range(3, 3+signs_num):
        small_list[j] = randint(0, 3)

    # 生成运算数
    for j in range(6, 6+signs_num+1):
        small_list[j] = Fraction(randint(0, r), randint(1, r))

    return small_list

def generate_fin(r:int):
# 生成一个完整的small_list
    small_list = generate_loop(r)
    small_list = list_to_small_list(small_list)
    # 答案为None时，重新生成
    if small_list == None:
        return generate_fin(r)
    return small_list

def list_to_small_list(small_list: list):
# 根据small_list的前10个元素生成一个完整的small_list
    text = transform(small_list)
    ans = re_calculate(text)
    # 答案为None时，返回None
    if ans == None:
        return None
    small_list.append(text)
    small_list.append(ans)
    return small_list

def generate(n: int, r: int):
# 运算符数量（0）(1~3)
# 括号位置（1~2）(1~5)
# 运算符（3~5）(0~3，对应+-*/)
# 运算数（6~9）(Fraction)
# 字符串（10）(+-/*假分数，输出时需要转换为真分数)
# 答案（11）(Fraction)
# 空的补零

    l = [[n, r]]

    for i in range(n):
        small_list = generate_fin(r)
        while small_list[11] > r or small_list[11].denominator > r:
            small_list = generate_fin(r)
            for j in range(1, i):  
            # 检查是否重复
            # 当答案和运算符重复时，认为这两个算式是重复的
                if small_list[11] == l[j][11]:
                    list_1 = paixu(small_list[3:6])
                    list_2 = paixu(l[j][3:6])
                    if list_1 == list_2:
                        ans = -1
                        break
            


        l.append(small_list)
    return l


def paixu(l: list):
    for i in range(1, len(l)):
        for j in range(1, len(l)-i):
            if l[j] > l[j+1]:
                l[j], l[j+1] = l[j+1], l[j]
    return l

