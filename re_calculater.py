import re
from fractions import Fraction


def str2calculate(text: str):
    # 将字符串中的运算符转为可识别的符号
    text = text.replace('÷', '/')
    text = text.replace('×', '*')
    text = text.replace('−', '-')
    return text


def calculate2str(text: str):
    # 将字符串中的运算符转为符合格式要求的符号
    text = text.replace(' / ', ' ÷ ')
    text = text.replace('*', '×')
    text = text.replace('-', '−')
    return text


def improper2proper(text: str):
    # 字符串下，假分数转为真分数
    n = re.findall(r'(\d+)/(\d+)', text)
    m = []
    for item in n:
        a = int(item[0])
        b = int(item[1])
        if a > b:
            m.append(str(a // b) + '’' + str(a % b) + '/' + str(b))
        else:
            m.append(str(a) + '/' + str(b))
    for i in range(len(n)):
        text = text.replace(n[i][0] + '/' + n[i][1], m[i], 1)
    return text


def proper2improper(text: str):
    # 字符串下，真分数转为假分数
    n = re.findall(r'(\d+)’(\d+)/(\d+)', text)
    m = []
    for item in n:
        a = int(item[0])
        b = int(item[1])
        c = int(item[2])
        m.append(str(a * c + b) + '/' + str(c))
    for i in range(len(n)):
        text = text.replace(n[i][0] + '’' + n[i][1] + '/' + n[i][2], m[i])
    return text


def re_calculate(text: str):
    # 输入并计算字符串，返回一个Fraction对象
    # 表达式格式：
    # 不支持小数、负数、带分数
    # 运算符两侧有空格，支持加减乘除：+-*/
    # 支持括号，注意括号不要靠在运算符两侧，确保运算符可以被正确识别：(1 + 2) * 3
    # 支持假分数，分数符号两侧不要留空格：3/2 + 1/2
    # 出现负数或除以0时，返回None

    # 匹配仅有2个运算数的表达式
    # 包含开头和末尾的括号
    n = re.match(r'^\(*\d+(/\d+)? [+\-*/] \d+(/\d+)?\)*$', text)
    if n:
        # 将分数转换为可被eval()计算的形式
        # 分数
        # 这一步可以避免除法和分数同时出现时被识别成连续除法
        text = re.sub(r'(\d+)/(\d+)', r'Fraction(\1,\2)', text)
        # 整数
        text = re.sub(r'(\d+) ', r'Fraction(\1)', text)
        text = re.sub(r' (\d+)', r'Fraction(\1)', text)
        # 除以0的情况
        try:
            ans = eval(text)
        except:
            return None
        # 出现负数的情况
        if ans < 0:
            return None
        else:
            return ans

    # 匹配括号
    # 计算括号内的数值，并替换回原字符串
    n = re.search(r'\((.*\d+ [+\-*/] \d+.*)\)', text)
    while n:
        # 计算时不含括号
        brackets = re_calculate(n.group(1))
        if brackets is None:
            return None
        # 替换时包含括号（即消除这个括号）
        text = text.replace(n.group(), str(brackets), 1)
        n = re.search(r'\(.*\d+ [+\-*/] \d+.*\)', text)

    # 匹配乘除
    # 此时式子中不包含乘除
    # 从左到右计算乘除，并替换回原字符串
    # 此时是在调用re_calculate()中的第一种情况（仅包含两个运算数）
    n = re.search(r'\d+(/\d+)? [*/] \d+(/\d+)?', text)
    while n:
        multiply = re_calculate(n.group())
        if multiply is None:
            return None
        text = text.replace(n.group(), str(multiply), 1)
        n = re.search(r'\d+(/\d+)? [*/] \d+(/\d+)?', text)

    # 匹配加减
    # 此时式子中不包含括号、乘除
    # 从左到右计算加减，并替换回原字符串
    # 此时是在调用re_calculate()中的第一种情况（仅包含两个运算数）
    n = re.search(r'\d+(/\d+)? [+\-] \d+(/\d+)?', text)
    while n:
        add = re_calculate(n.group())
        if add is None:
            return None
        text = text.replace(n.group(), str(add), 1)
        n = re.search(r'\d+(/\d+)? [+\-] \d+(/\d+)?', text)

    # 返回一个分数结果
    return Fraction(text)
