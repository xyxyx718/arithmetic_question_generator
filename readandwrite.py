from transformer import fraction2str


def output(l: list):
    text = ''
    for i in range(1, l[0][0]+1):  # n
        text = text+'%d. ' % i  # 序号
        text = text+l[i][10]  # 题目
        text = text + ' =\n'  # 等号和换行

    ans_text = ''
    for i in range(1, l[0][0]+1):  # n
        ans_text = ans_text+'%d. ' % i  # 序号
        ans_text = ans_text+fraction2str(l[i][11])  # 答案
        ans_text = ans_text + '\n'  # 换行

    return text, ans_text

def write_file(text: str, path: str):
    try:
        with open(r'%s' % path, mode='w', encoding='utf-8') as f:
            f.write('%s' % text)
    except:
        return -1
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