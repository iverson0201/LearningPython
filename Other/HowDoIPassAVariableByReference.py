#!/usr/bin/python
#encoding=utf-8

'''
Arguments are passed by assignment(https://docs.python.org/2.7/faq/programming.html#id18).
The rationale behind this is twofold:
    1. the parameter passed in is actually a reference to an object (but the reference is passed by value)
    2. some data types are mutable, but others aren't
    So:
        1. If you pass a mutable object into a method, the method gets a reference 
        to that same object and you can mutate it to your heart's delight, 
        but if you rebind the reference in the method, the outer scope will 
        know nothing about it, and after you're done, the outer reference will still point at the original object.
        ( 如果传入方法的是一个可以修改的对象，那么方法得到对象的引用且可以愉快地修改它,
         但是如果你重新绑定引用在方法中，外部作用域将无法了解对于重新绑定引用, 因此你这样做之后,
         外部引用将还是指向原对象)
        2. If you pass an immutable object to a method, you still can't 
        rebind the outer reference, and you can't even mutate the object.
    To make it even more clear, let's have some examples.
'''

# List - a mutable type
def try_to_change_list_content(the_list):
    print 'got', the_list
    the_list.append('four')
    print 'change to', the_list

outer_list = ['one', 'two', 'three']
print 'before, outer_list', outer_list
try_to_change_list_content(outer_list)
print 'after, outer_list', outer_list

print '--------------------------------------------------------------'

def try_to_change_list_reference(the_list):
    print 'got', the_list
    the_list = ['and', 'we', 'can', 'not', 'lie']
    print 'set to', the_list

outer_list = ['we', 'like', 'proper', 'english']
print 'before, outer_list', outer_list
try_to_change_list_reference(outer_list)
print 'after, outer_list', outer_list
