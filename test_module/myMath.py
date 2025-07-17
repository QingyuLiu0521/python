def mySquare(x):
    return x * x

# 如果模块被直接运行，__name__的值为'__main__'
# 如果模块被导入，__name__的值为模块名
if __name__ == '__main__':
    # 只有直接运行该py，才会执行下面的语句
    print(mySquare(3))