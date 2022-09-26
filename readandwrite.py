from re_calculater import calculate2str, improper2proper
from re_calculater import str2Calculate, proper2improper
import re


def output_format(l: list):
    # 将l中的内容格式化成可以输出到文件的形式
    # 返回2个字符串，
    text = ''
    for i in range(1, l[0][0]+1):  # n
        text = text + '%d. ' % i  # 序号
        question = l[i][10]
        question = improper2proper(question)
        question = calculate2str(question)
        text = text + question  # 题目
        text = text + ' =\n'  # 等号和换行

    ans_text = ''
    for i in range(1, l[0][0]+1):  # n
        ans_text = ans_text + '%d. ' % i  # 序号
        # 答案
        ans = l[i][11]
        ans = improper2proper(str(ans))
        ans_text = ans_text + ans
        ans_text = ans_text + '\n'  # 换行

    return text, ans_text


def input_fromat(text: str, type='e'):
    # 将文件内容格式化成可以计算的形式
    # 返回一个列表
    if type == 'e':
        exercises = re.findall(r'\d+\. ([ 0-9\+−×÷/’\(\)]+)=[ \n$]+', text)
        for i in range(len(exercises)):
            exercises[i] = str2Calculate(exercises[i])
            exercises[i] = proper2improper(exercises[i])
        return exercises
    elif type == 'a':
        answers = re.findall(r'\d+\. ([ 0-9/’]+)[ \n$]+', text)
        for i in range(len(answers)):
            answers[i] = str2Calculate(answers[i])
            answers[i] = proper2improper(answers[i])
        return answers
    else:
        return -1


def write_file(text: str, path: str):
    try:
        with open(r'%s' % path, mode='w', encoding='utf-8') as f:
            f.write('%s' % text)
    except:
        return -1

    return 0
# 文件只读或其他错误


def read_file(path: str):
    # 读取文件
    try:
        with open(r'%s' % path, mode='r', encoding='utf-8') as f:
            text = f.read()
    except:
        try:
            with open(r'%s' % path, mode='r', encoding='gbk') as f:
                text = f.read()
        except:
            return -1

    return text
