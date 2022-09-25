def fraction2str(fraction):
    i = int(fraction)
    if i > 0:
        f = fraction-i
        if f == 0:
            return str(i)
        else:
            return '%d’' % i+str(f)
    else:
        return str(fraction)

# 将small_list[0:9]转换为字符串
def transform(small_list):
    signs = ['+', '−', '×', '÷']
    text = ''

    if small_list[1] == 0:  # 无括号
        text = text + fraction2str(small_list[6])  # 第一个运算数
        for j in range(small_list[0]):
            text = text + \
                ' %s ' % signs[small_list[j+3]] + \
                fraction2str(small_list[j+7])  # 每组运算符和运算数各一个

    else:  # 有括号
        kuohao = 1  # 1左括号 2右括号
        if small_list[1] == 1:
            text = text + '('
            kuohao = 2
        text = text + fraction2str(small_list[6])  # 第一个运算数
        for j in range(small_list[0]):
            if kuohao == 2 and j+2 == small_list[2]:  # 右括号
                text = text + ')'
                kuohao = 3
            text = text + ' %s ' % signs[small_list[j+3]]  # 运算符
            if kuohao == 1 and j+2 == small_list[1]:  # 左括号
                text = text + '('
                kuohao = 2
            text = text + fraction2str(small_list[j+7])  # 运算数
        if kuohao == 2:  # 右括号
            text = text + ')'
    return text
