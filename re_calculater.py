import re
from fractions import Fraction


def str2Calculate(text: str):
    text = text.replace('÷', '/')
    text = text.replace('×', '*')
    text = text.replace('−', '-')
    return text


def calculate2str(text: str):
    text = text.replace('/', '÷')
    text = text.replace('*', '×')
    text = text.replace('-', '−')
    return text


def improper2proper(text: str):
    n = re.search(r'^(\d+)/(\d+)', text)
    if n==None:
        n = re.search(r'[ \(](\d+)/(\d+)', text)
    while n:
        f = Fraction(int(n.group(1)), int(n.group(2)))
        x = int(f)
        f = f - x
        if f>0:
            text = text.replace(n.group(1)+'/'+n.group(2), str(x) + "’" + str(f))
        else:
            text = text.replace(n.group(1)+'/'+n.group(2), str(x))
        n = re.search(r'[^’](\d+)/(\d+)', text)
    return text


def fraction2str(fraction: Fraction):
    if fraction.denominator == 1:
        return str(fraction.numerator)
    return str(fraction.numerator) + '/' + str(fraction.denominator)


def str2Fraction(text: str):
    n = re.search(r'\d+(/\d+)?', text)
    if n:
        return Fraction(n.group())
    return None


def re_calculate(text: str):
    n = re.match(r'^\(*\d+(/\d+)? [\+\-\*/] \d+(/\d+)?\)*$', text)
    if n:
        text = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', text)
        text = re.sub(r'(\d+)', r'Fraction(\1)', text)
        try:
            ans = eval(text)
        except:
            return None
        return ans
    n = re.search(r'\((.*\d+ [\+\-\*/] \d+.*)\)', text)

    while n:
        brackets = re_calculate(n.group(1))
        if brackets == None:
            return None
        text = text.replace(n.group(), str(brackets), 1)
        n = re.search(r'\(.*\d+ [\+\-\*/] \d+.*\)', text)

    n = re.search(r'\d+(/\d+)? [\*/] \d+(/\d+)?', text)
    while n:
        multiply = re_calculate(n.group())
        if multiply == None:
            return None
        text = text.replace(n.group(), str(multiply), 1)
        n = re.search(r'\d+(/\d+)? [\*/] \d+(/\d+)?', text)

    n = re.search(r'\d+(/\d+)? [\+\-] \d+(/\d+)?', text)
    while n:
        add = re_calculate(n.group())
        if add == None or add < 0:
            return None
        text = text.replace(n.group(), str(add), 1)
        n = re.search(r'\d+(/\d+)? [\+\-] \d+(/\d+)?', text)

    return str2Fraction(text)


if __name__ == '__main__':
    s = '(8 / 1/10 - (3 + 4) * 10) / 3'
    a = re_calculate(s)
    print(a)
    print(improper2proper(str(a)))
