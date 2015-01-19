#!/usr/bin/env python
# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import re
import chardet

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def Getpage():
    url = u'http://www.amazon.cn/gp/feature.html/ref=sa_menu_kindle_l3_f126758?ie=UTF8&docId=126758'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-agent' : user_agent }
    req = urllib2.Request(url, headers = headers)
    try:
        myResponse = urllib2.urlopen(req)
    except URLError, e:
        if hasatter(e, 'code'):
            print 'Error code is:', code
        elif hasatter(e, 'reason'):
            print 'Error reason is:', e.reason
    myPage = myResponse.read()

    charset = chardet.detect(myPage)
    charset = charset['encoding']
    print charset
    if charset == 'utf-8' or charset == 'UTF-8':
        myPage = myPage
    else:
        myPage = myPage.decode('gb2312', 'ignore').encode('utf-8')
    unicodePage = myPage.decode('utf-8')
    
    my_url = re.search(ur'<table.*?<b>Kindle今日特价书</b>.*?</table>', unicodePage, re.S)
    if my_url != None:
        my_url = my_url.group()
    else:
        return None

    book_match = ur'.*alt="(.*?)-Kindle电子书今日特价-亚马逊".*alt="(.*?)-Kindle电子书今日特价-亚马逊".*alt="(.*?)-Kindle电子书今日特价-亚马逊".*alt="(.*?)-Kindle电子书今日特价-亚马逊".*'

    book_result = re.search(book_match, my_url, re.S)
    
    introduction_head = ur'.*<a href="(/gp/product.*?)"><img src="(http://ec4.*?)".*?alt="' 
    introduction_tail = ur'.*?</a>(.*?)<p><p><b>Kindle电子书价格.*?<span class="price">(.*?)</span>'
    introduction_match = ''
    for i in range(1, 5):
        introduction_match += introduction_head
        introduction_match += book_result.group(i)
        introduction_match += introduction_tail
    
    introduction_result = re.search(introduction_match, my_url, re.S)
    if introduction_result == None:
        return None
    result = {}
    for i in range(1, 5):
        result[i - 1] = [
            book_result.group(i),
            introduction_result.group(1 + (i - 1) * 4),
            introduction_result.group(2 + (i - 1) * 4),
            introduction_result.group(3 + (i - 1) * 4),
            introduction_result.group(4 + (i - 1) * 4),
            ]
    #    print introduction_result.group(1 + (i -1) * 4)
    return result

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((\
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, unicode) else addr))
    
def send_to_me_mail(book):

    from_addr = "qianlv7@qq.com"
    passwd = "xxxxxxx"
    to_addr = "qianlv7@qq.com"
    stmp_server = "smtp.qq.com"

    my_msg = u''
    if book != None:
        my_msg += u'<html><body>'
        for i in range(4):
            v = book[i]
            msg_format = u'<a href="http://www.amazon.cn%s">%s</a><br/> <img src="%s"> <br/> Introdution:<br /> %s <br /> Price: %s <br /> <br />' % (v[1], v[0], v[2], v[3], v[4])
            my_msg += msg_format
        my_msg += u'</body></html>'
    else:
        my_msg = '<html></body>Kindle特价书脚本出错注意查看</body></html>'


    msg = MIMEText(my_msg, 'html', 'utf-8')
    msg['From'] = _format_addr(u'Kindle特价书脚本<%s>' % from_addr)
    msg['To'] = _format_addr(u'浅绿 <%s>' % to_addr)
    msg['Subject'] = Header(u'Kindle特价书', 'utf-8').encode()

    server = smtplib.SMTP(stmp_server, 25)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(from_addr, passwd)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


if __name__ == '__main__':
    result = Getpage()
    send_to_me_mail(result)


