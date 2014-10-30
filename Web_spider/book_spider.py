#!/usr/bin/python
# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import thread
import re
import chardet

def delete_blank_line(txt):
    ret = ""
    for line in txt.split("\n"):
        if line.strip() != '':
            ret += line + "\n\n"
    return ret

def save_page(title, content):
    try:
        with open(title.strip(), "wb") as file:
            file.write(title + '\n')
            file.write(content)
    except Exception, e:
        print Exception, ':', e

class Book_spider:
    def __init__(self):
        self.pages = [] 
        self.page = 1
        self.flag = True 
        self.next_url = "http://www.ybdu.com/xiaoshuo/0/910/59302.html"
        self.pre_url =""

    def GetPage(self):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-agent' : user_agent }
        req = urllib2.Request(self.next_url, headers = headers)
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
        if charset == 'utf-8' or charset == 'UTF-8':
            myPage = myPage
        else:
            myPage = myPage.decode('gb2312', 'ignore').encode('utf-8')
        unicodePage = myPage.decode('utf-8')

        my_url = re.search(r'<a.*href="(.*)".*?id=\'pager_next\'.*?>', unicodePage, re.S)
        if my_url != None:
            my_url = my_url.group(1)
        self.next_url = my_url
        my_url = re.search(r'<a.*href="(.*)".*?id=\'pager_prev\'.*>', unicodePage, re.S)
        if my_url != None:
            my_url = my_url.group(1)
        self.pre_url = my_url

        my_title = re.search(r'<h1>(.*)</h1>', unicodePage, re.S)
        my_title = my_title.group(1)

        my_content = re.search(r'<div.*?id="htmlContent".*?class="contentbox">(.*?)</div>', unicodePage, re.S)
        my_content = my_content.group(1)

        my_content = my_content.replace("<br />", "\n")
        my_content = my_content.replace("&nbsp;", " ")
        my_content = my_content.replace("\r", "")
        my_content = re.search(r'(.*?)<',my_content, re.S)
        my_content = my_content.group(1)
        my_content = delete_blank_line(my_content)

        save_page(my_title, my_content)

        
        onPage = { 'title' : my_title, 'content' : my_content }
        return onPage

    def LoadPage(self):
        while self.flag:
            if (len(self.pages) - self.page < 3):
                try:
                    myPage = self.GetPage()
                    self.pages.append(myPage)
                except (KeyError, ValueError):
                    print 'cann\'t get Page'

    def ShowPage(self, curPage):
        print curPage['title']
        print curPage['content']
        print "\n"
        user_input = raw_input("当前阅读%d章节, 回车阅读下一章或输入 quit 退出" % self.page)
        if user_input == 'quit':
            self.flag = False
        print '\n'

    def Start(self):
        print u'开始阅读...'
        thread.start_new_thread(self.LoadPage,())
        while self.flag:
            if self.page <= len(self.pages):
                nowPage = self.pages[self.page - 1]
                self.ShowPage(nowPage)
                self.page = self.page + 1

if __name__ == '__main__':
    print u"""
    ——————————————————————————
    按下回车开始
    _________________________
    """
    print u"请按下回车..."
    raw_input()
    myBook = Book_spider()
    myBook.Start()

