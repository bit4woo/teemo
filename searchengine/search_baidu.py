# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib import myparser
from lib.log import logger
import time
from lib import myrequests
req = myrequests

class search_baidu:

    def __init__(self, word, limit, proxy=None):
        self.engine_name ="Baidu"
        self.word = word
        self.limit = int(limit)
        self.results = ""
        self.totalresults = ""
        self.proxies = proxy
        self.server = "www.baidu.com"
        self.counter = 0 #
        self.print_banner()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def do_search(self):
        try:
            url = "http://{0}/s?wd={1}&pn={2}".format(self.server,self.word,self.counter)# 这里的pn参数是条目数
            r = req.get(url, proxies = self.proxies)
            self.results = r.content
            self.totalresults += self.results
            return True
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return False

    def process(self):
        while self.counter <= self.limit and self.counter <= 1000:
            if self.do_search():
                time.sleep(1)
                #print "\tSearching " + str(self.counter) + " results..."
                self.counter += 10
                continue
            else:
                break

    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        #print "%s email(s) found in Baidu" %len(rawres.emails())
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        #print "%s domain(s) found in Baidu" %len(rawres.hostnames())
        return rawres.hostnames()
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        logger.info("{0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e)))
        return self.d, self.e


if __name__ == "__main__":
        useragent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        proxy = {"http":"http://127.0.0.1:8080"}
        search = search_baidu("meizu.com", '100',proxy)
        print search.run()
