#!/usr/bin/python
#encoding=utf-8

import urllib2
import sys
import re
import base64
from urlparse import urlparse

# The two normal authentication schemes are basic and digest authentication. 
# Between these two, basic is overwhelmingly the most common. 
# As you might guess, it is also the simpler of the two.
# 
# A summary of basic authentication goes like this :
#
#     1.client makes a request for a webpage
#     2. server responds with an error(Error code is 401 and 
#        The 'WWW-Authenticate' header line looks like ' WWW-Authenticate: SCHEME realm="REALM" ',requesting authentication)
#     3.client retries request - with authentication details encoded in request
#       This is request include Username/Password by encoding it as base 64 string(Base64)
#     4.server checks details and sends the page requested, or another error
# The more detail: http://www.voidspace.org.uk/python/articles/authentication.shtml
def getHeader():
    
    username = 'username'
    password = 'xxxxxxxx'

    url = "http://api.minicloud.com.cn/statuses/friends_timeline.xml" #一个需要basic authentication验证的页面
    #url = "http://www.baidu.com"
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-agent' : user_agent }
    req = urllib2.Request(url, headers = headers)

    try:
        response = urllib2.urlopen(req)
        print response.headers
    except IOError, e:
        pass
    else:
        #没有异常就是一个正常的页面
        print 'This page isn\'t protected by authentication'
        sys.exit(1)
    
    if not hasattr(e, 'code') or e.code != 401:
        #we get a error - but not a 401 error
        print 'This page isn\'t protected by authentication'
        print 'code :', e.code
        print 'reason :', e.reason
        sys.exit(1)

    print e.headers
    authline = e.headers['www-authenticate']
    print authline
    
    authobj = re.compile( \
            r'''(?:\s*www-authentication\s*:)?\s*(\w*)\s+realm=['"]([^'"]+)['"]''',\
            re.IGNORECASE)#忽略大小写
    mathobj = authobj.match(authline)

    if not mathobj:
        #无法匹配返回头部有问题
        print 'The authentication header is badly formed'
        print authline
        sys.exit(1)

    #获取头部的配置
    scheme = mathobj.group(1)
    realm = mathobj.group(2) 

    if schemes.lower() != 'basic':
        print 'this example only works with BASIC authentication'
        sys.exit(1)

    if authline.lower() != 'basic':
         print 'this example only works with BASIC authentication'
         sys.exit(1)

    base64string = base64.encodestring('%s:%s' % (username, password))[:-1] 
    #base64.encodestring生成的字符串会在最后加入换行,要去掉
    authheader = "Basic %s" % base64string
    req.add_header("Authorization", authheader)

    try:
        response = urllib2.urlopen(req)
    except IOError, e:
        #此处异常用户名或密码错误
        print "It look like the Username or Password is wrong."
        sys.exit(1)

    page = response.read()
    print page

        
if __name__ == '__main__':
    getHeader()
