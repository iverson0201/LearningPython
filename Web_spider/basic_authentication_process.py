#!/usr/bin/python
#encoding=utf-8

import sys
import urllib2

# 关于urllib2参考:
# https://docs.python.org/2.7/library/urllib2.html?highlight=urllib2#urllib2.OpenerDirector
# http://www.voidspace.org.uk/python/articles/urllib2.shtml
# http://blog.csdn.net/pleasecallmewhy/article/details/8924889
url = ""
username = 'username'
password = 'xxxxxxxx'

# 创建一个密码管理器
password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()

# 如果知道realm,可以用它代替'None'
# HTTPBasicAuthHandler使用一个密码管理的对象来处理URLs和realms来映射用户名和密码。
# 如果你知道realm(从服务器发送来的头里)是什么，你就能使用HTTPPasswordMgr。
# 
# 通常人们不关心realm是什么。那样的话，就能用方便的HTTPPasswordMgrWithDefaultRealm。
# 这个将在你为URL指定一个默认的用户名和密码。
password_manager.add_password(None, url, username, password)

# 创建一个handler
hanler = urllib2.HTTPBasicAuthHandler(password_manager)

# 创建"opener" (OpenerDirector实例)
opener = urllib2.build_opener(handler)

# 这里有两种选择
# 1. 使用实例的opener的open处理url, 及opener.open(url/request object, [data, [timeout]])
# 2. 安装这个opener， 使得调用urllib2.urlopen 将用我们的opener

urllib2.install_opener(opener)
