from cgi import print_arguments
from random import randint
from fractions import Fraction
from turtle import position
from transformer import transform
from calculater import calculate
import re


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


def generate(n: int, r: int):
    l = [[n, r]]

    for i in range(n):
        small_list = generate_loop(r)
        text = transform(small_list)
        ans = calculate(text)
        small_list.append(text)
        small_list.append(ans)

        while ans > r or ans.denominator > r or zero_check(small_list) == -1:
            small_list = generate_loop(r)
            text = transform(small_list)
            ans = calculate(text)
            small_list.append(text)
            small_list.append(ans)
            for j in range(1, i):  # 检查是否重复
                if ans == l[j][11]:
                    list_1 = paixu(small_list[3:6])
                    list_2 = paixu(l[j][3:6])
                    if list_1 == list_2:
                        ans = -1

        l.append(small_list)
    return l


def paixu(l: list):
    for i in range(1, len(l)):
        for j in range(1, len(l)-i):
            if l[j] > l[j+1]:
                l[j], l[j+1] = l[j+1], l[j]
    return l

def list_to_small_list(small_list: list):
    text = transform(small_list)
    ans = calculate(text)
    small_list.append(text)
    small_list.append(ans)
    return small_list

# 负数检查
# 返回参数：0 无负数，-1 有负数
def zero_check(small_list: list):
    # 如果答案是负数
    if small_list[11] < 0:
            return -1
    # 没有负号
    ok = 0
    for i in range(3,6):
        if small_list[i] == 1:
            ok = -1
    if ok != -1:
        return 0
    
    # 有负号
    # 1个运算符
    # 直接看答案
    if small_list[0] == 1:
        return 0
        
    
    # 2个运算符 无括号
    ok = 0
    for i in range(3,6):
        if small_list[i] > 1:
            ok = -1
    # ok=0时，没有乘除        
    if ok == 0 and small_list[0] == 2:
        
        small_list_1 = [1, 0,0,small_list[3],0,0,small_list[6],small_list[7],0,0]
        small_list_1 = list_to_small_list(small_list_1)

        if zero_check(small_list_1) == -1:
            return -1

        small_list_2 = [1, 0,0,small_list[4],0,0,small_list_1[11],small_list[8],0,0]
        small_list_2 = list_to_small_list(small_list_2)

        if zero_check(small_list_2) == -1:
            return -1
        else:
            return 0
    # ok=-1时，有乘除
    if ok == -1 and small_list[0] == 2:
        if small_list[11] < 0:
            return -1
        else:
            return 0
    # 2个运算符 有括号
    # 减号必定在括号里面
    if small_list[0] == 2 and small_list[1] != 0:
        location = re.search(r'\((.*)\)', small_list[10])
        text = small_list[10][location.start()+1:location.end()-1]
        if calculate(text) < 0:
            return -1
        else:
            return 0
    

    # 3个运算符 有括号
    
    if small_list[0] == 3 and small_list[1] != 0:
        # 括号里面有两个数
        if small_list[2]-small_list[1] == 2:
            # 把括号里面的数提出来
            # 如果是负数就 return -1
            location = re.search(r'\((.*)\)', small_list[10])
            text = small_list[10][location.start()+1:location.end()-1]
            kuohao = calculate(text)
            if kuohao < 0:
                return -1
            
            # 把提出来的数放回去
            # 然后直接做zero_check
            small_list_1 = [2,0,0,0,0,0,0,0,0,0]
            j=3
            for i in range(3,6):
                if i!=2+small_list[1]:
                    small_list_1[j]=small_list[i]
                    j=j+1
            j=6
            for i in range(6,10):
                if i == 5+small_list[1]:
                    small_list_1[j]=kuohao
                    j=j+1
                elif i != 6+small_list[1]:
                    small_list_1[j]=small_list[i]
                    j=j+1
            small_list_1 = list_to_small_list(small_list_1)

            x = zero_check(small_list_1)
            if x == -1:
                return -1
            else:
                return 0
        
        # 括号里面有三个数
        # 减号必定在括号里面
        else:
            small_list_1 = [2,0,0,0,0,0,0,0,0,0]
            j=3
            for i in range(2+small_list[1],4+small_list[1]):
                small_list_1[j]=small_list[i]
                j=j+1
            j=6
            for i in range(5+small_list[1],8+small_list[1]):
                small_list_1[j]=small_list[i]
                j=j+1
            small_list_1 = list_to_small_list(small_list_1)

            x = zero_check(small_list_1)
            if x == -1:
                return -1
            else:
                return 0
    
    # 3个运算符 无括号

    if small_list[0] == 3 and small_list[1] == 0:
        # 检测乘除
        ok = 0
        for i in range(3,6):
            if small_list[i] > 1:
                ok = -1
                break
        # ok=0时，没有乘除
        if ok == 0:
            small_list_1 = small_list.copy()
            for i in range(7,10):
                if small_list_1[i-3] == 0:
                    small_list_1[i] = small_list[i-1]+small_list[i+1]
                elif small_list_1[i-3] == 1:
                    small_list_1[i] = small_list[i-1]-small_list[i+1]
                if small_list_1[i] < 0:
                    return -1
            return 0
        # ok=-1时，有乘除
        # 有且只有一个乘除
        # 在乘除两边加上括号，丢回zero_check里面
        else:
            for i in range(3,6):
                if small_list[i] > 1:
                    break
            small_list_1 = small_list[0:10].copy()
            small_list_1[1]=i-2
            small_list_1[2]=i
            small_list_1 = list_to_small_list(small_list_1)
            x = zero_check(small_list_1)
            if x == -1:
                return -1
            else:
                return 0