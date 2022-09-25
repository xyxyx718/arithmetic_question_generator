import re
from fractions import Fraction

def calculate(text:str):

    text = text.replace('÷', '/')
    text = text.replace('×', '*')
    text = text.replace('−', '-')
    text = text.replace(' ', '')

    text = re.sub(r'(\d+)’(\d+\/\d+)', r'(\1+\2)', text)
    text = re.sub(r'(\d+)', r'Fraction(\1)', text)

    try:
        ans = eval(text)
    except:
        ans = -1
    
    return ans
    # 除以0会报错