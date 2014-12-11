#/usr/bin/python
#encoding=utf-8
'''
4.1 python 对象三个特性: an identity, a type, and a value.
    identity : 每个对象的唯一身份标识自己， id() 返回对象内存地址
    type : 类型, type() 返回对象类型
    value : 数据项
4.2 所有对象都可以进行布尔测试， 同类型的对象之间可以比较大小
下列对象布尔值是False:
    1. None 2. False 
    3. Any numberic zero: 0, 0.0, 0L, 0.0+0.0j(complex)
        "", [], (), {}
    4. 实现了__nonzero__() 或 __len__()方法且方法放回0或False, 那么
       它的实例当作False
'''
def test_bool(value):
    if value:
        print 'True'
    else:
        print 'False'
class len_zero(object):
    # len() 时调用
    def __init__(self,value):
        self.value = value
    def __len__(self):
        return 0
    # 通常在用类进行判断和将类转换成布尔值时调用
    def __nonzero__(self):
        print 'in nonzero'
        return False 

test_bool(1)
test_bool([])
test_bool(len(len_zero(1)))
test_bool(len_zero(1))




'''
4.4 内部类型:
    1. 代码对象
    2. 帧对象
    3. 跟踪记录对象
    4. 切片对象
    5. 省略对象
    6. xrange 对象
'''
# 4.5.1  对象值的比较(value)
one = len_zero(1)
two = len_zero(2)
print one < two
# 4.5.2 对象身份的比较(identity)
# 对象就像一个装有内容的盒子, 一个对象被赋值给一个变量，就像在这个
# 盒子上贴了一个标签,表示创建了一个引用. 每当这个对象有了一个新的引
# 用,就会在盒子上新贴一个标签。当一个引用被销毁时,这个标签就会被撕
# 撕掉，没有标签时就会被回收
# is 比较身份(内存地址(id)), 比较运算符(==, <, > 等)比较值
print '---------------------------------'
foo1 = foo2 = 4.3
print id(foo1), id(foo2), foo1 is foo2

foo1 = 4.3
foo2 = 1.3 + 3.0
foo3 = 4.3
fo1 = 1000000
fo2 = 1000000
fof1 = 9.342432432432432
fof2 = 9.342432432432432
print id(foo1), id(foo2), id(foo3)
print foo1 is foo2, foo1 is not foo2, foo1 is foo3
print foo1 == foo3
print "fo1 is fo2:", fo1 is fo2
print "fof1 is fof2:", fof1 is fof2
# 发现在脚本中foo1,foo3为同一个对象
# 如果在python交互终端中则不是同一个对象
# 原因:(比较小的整数 Python2.7 好像是[-5,256])整数对象的内存池。
# 字符串也有也有这个内存池,因此每个对象只存有一份.比如,所有
# 整数1的引用都指向同一对象
print '---------------------------------'

print repr(len_zero)
print str(len_zero)
print `len_zero`

