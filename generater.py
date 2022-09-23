from random import randint
from fractions import Fraction
from transformer import transform
from calculater import calculate


def generate_loop(r):
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
        if j > 0 and small_list[j-4] == 3:
            small_list[j] = Fraction(randint(1, r), randint(1, r))
        else:
            small_list[j] = Fraction(randint(0, r), randint(1, r))

    return small_list

# 运算符数量（0），括号位置（1~2），运算符是什么（3~5），运算数（6~9），字符串（10），答案（11），空的补零


def generate(n, r):
    l = [[n, r]]

    for i in range(n):
        small_list = generate_loop(r)
        text = transform(small_list)
        ans = calculate(text)

        while ans < 0 or ans > r:
            small_list = generate_loop(r)
            text = transform(small_list)
            ans = calculate(text)
            for j in range(1, i): # 检查是否重复
                if ans == l[j][11]:
                    list_1 = paixu(small_list[3:6])
                    list_2 = paixu(l[j][3:6])
                    if list_1 == list_2:
                        ans = -1
        small_list.append(text)
        small_list.append(ans)

        l.append(small_list)
    return l


def paixu(l: list):
    for i in range(1, len(l)):
        for j in range(1, len(l)-i):
            if l[j][11] > l[j+1][11]:
                l[j], l[j+1] = l[j+1], l[j]
    return l
