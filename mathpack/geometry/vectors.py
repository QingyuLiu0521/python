'''
向量运算模块
'''
from math import sqrt

class Vector2D:
    '''
    二维向量类
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def magnitude(self):    # 计算模
        return sqrt(self.x ** 2 + self.y ** 2)
    def dot(self, otherV): # 计算点积
        return (self.x * otherV.x + self.y + otherV.y)

class Vector3D:
    '''
    三维向量类
    '''
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    def dot(self, otherV):
        return (self.x * otherV.x + self.y * otherV.y + self.z * otherV.z)