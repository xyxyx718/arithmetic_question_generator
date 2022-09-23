import re

def calculate(text:str):
    text = text.replace('÷', '/')
    text = text.replace('×', '*')
    text = text.replace('−', '-')
    text = text.replace(' ', '')
    re.sub(r'(\d+)', r'Fraction(\1, 1)', text)
    return eval(text)