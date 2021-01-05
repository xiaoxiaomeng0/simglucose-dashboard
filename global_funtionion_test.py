a = 1
b = 2
# c = 3

# def testGlobal(a, b):
#     return a + b + c

class FOO:
    a = 7
    def __init__(self):
        self.a = 3
        self.b = 4
    
    def test(self):
        return self.a


foo = FOO()
print(foo.test())

# print(testGlobal(3, 4))
# print(c)