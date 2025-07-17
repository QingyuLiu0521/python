'''
基本数学运算模块
'''

def add(x, y):
    return x + y

def substract(x, y):
    return x - y
    
def multiply(x, y):
    return x * y

def divide(x, y):
    if (not y):
        raise ValueError("The divisor can not be zero!")
    return x / y