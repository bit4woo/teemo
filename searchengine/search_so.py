# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
from lib import myparser
import re
from lib.log import logger
from lib import myrequests
req = myrequests
#核心方法之一，没有请求限制，无需要代理


class search_so():

    def __init__(self, word, limit, proxy=None):
        self.engine_name = "360SO"
        self.word = word.replace(' ', '%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" #所有搜索结果
        self.server = "www.so.com"
        self.limit = int(limit)
        self.counter = 1 #page number  ---> page 参数
        self.proxies = proxy
        self.print_banner()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def do_search(self):
        try:#https://www.so.com/s?q={query}&pn={page_no}
            url = "https://{0}/s?q={1}&pn={2}".format(self.server,self.word,self.counter) #  %40=@ 搜索内容如：@meizu.com;在关键词前加@有何效果呢？，测试未发现不同
            r = req.get(url, proxies = self.proxies,verify=False)
            self.results = r.content
            self.totalresults += self.results
            return True
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return False

    def check_next(self):
        renext = re.compile('snext')
        nextres = renext.findall(self.results)
        if nextres != []:
            return True
        else:
            return False

    def process(self):
        while (self.counter < self.limit/10): #limit = item number; counter= page number ... 10 items per page
            if self.do_search():
                if self.check_next():
                    self.counter += 1
                    continue
                else:
                    break
            else:
                break
    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        logger.info("{0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e)))
        return self.d, self.e


if __name__ == "__main__":
    proxy = {"http":"http://127.0.0.1:8080"}
    useragent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
    search = search_so("meizu.com", '100',proxy)
    print search.run()