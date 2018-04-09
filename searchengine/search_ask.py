# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
from lib import myparser
from lib.log import logger
import re
from lib import myrequests
req = myrequests

#核心方法之一，没有请求限制，只是需要代理

class search_ask():

    def __init__(self, word, limit, proxy=None):
        self.engine_name = "Ask"
        self.word = word.replace(' ', '%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" #所有搜索结果
        self.server = "www.ask.com"
        #self.quantity = "100" #useless
        self.limit = int(limit)  #item number?
        self.counter = 0 #page number  ---> page 参数
        self.proxies = proxy
        self.print_banner()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def do_search(self):
        try:
            url = "http://{0}/web?q=site:{1}&pu=100&page={2}".format(self.server, self.word,self.counter)  # %40=@ 搜索内容如：@meizu.com;在关键词前加@有何效果呢？，测试未发现不同
            r = req.get(url, proxies = self.proxies)
            #如果不指定header， agent的值将如下 ：  User-Agent: python-requests/2.18.1  这对有请求限制的搜索引擎很关键，比如google
            #采用随机user agent的话，
            self.results = r.content
            self.totalresults += self.results
            return True
        except Exception,e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return False

    def check_next(self):
        renext = re.compile('>Next<') #<li class="PartialWebPagination-next">Next</li>
        nextres = renext.findall(self.results)
        if nextres != []:
            nexty = "1"
        else:
            nexty = "0"
        return nexty

    def get_people(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.people_jigsaw()

    def process(self):
        while (self.counter < self.limit/100): #limit = item number; counter= page number ... 100 items per page
            if self.do_search():
                more = self.check_next()
                if more == "1":
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
    proxy = {"http":"http://127.0.0.1:9988"}
    useragent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
    search = search_ask("meizu.com", '1000')
    print search.run()