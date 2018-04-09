# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib import myparser
from lib.log import logger
import re
import time
import random
from lib import myrequests
req = myrequests

class search_yandex:

    def __init__(self, word, limit, proxy=None):
        self.engine_name = "Yandex"
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.server = "yandex.com"
        self.limit = int(limit)
        self.counter = 0
        self.proxies = proxy
        self.print_banner()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def do_search(self):
        try:
            url = "http://{0}/search?text={1}&numdoc=50&lr=10590&pn={2}".format(self.server,self.word,self.counter) #  %40=@ 搜索内容如：@meizu.com;在关键词前加@有何效果呢？，测试未发现不同
            r = req.get(url, proxies=self.proxies)
            if "automated requests" in r.content:
                logger.warning("Yandex blocked our request")
                return False
            else:
                self.results = r.content
                self.totalresults += self.results
                return True
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return False

    def do_search_files(self, files):  # TODO
        url = "http://{0}/search?text=%40{1}&numdoc=50&lr={2}".format(self.server,self.word,self.counter)
        req.get(url)

    def check_next(self):
        renext = re.compile('topNextUrl')
        nextres = renext.findall(self.results)
        if nextres != []:
            return True
        else:
            return False

    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()

    def get_files(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.fileurls(self.files)

    def process(self):
        while self.counter <= self.limit and self.counter<500:
            if self.do_search():
                if self.check_next():
                    time.sleep(random.randint(1, 5))
                    self.counter += 1
                    continue
                else:
                    break
            else:
                break

    def process_files(self, files):
        while self.counter < self.limit and self.counter<500:
            self.do_search_files(files)
            time.sleep(0.3)
            self.counter += 50
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        logger.info("{0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e)))
        return self.d, self.e

if __name__ == "__main__":
        print "[-] Searching in Bing:"
        useragent = "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
        proxy = {"http": "http://127.0.0.1:9988"}
        search = search_yandex("meizu.com", 500, proxy)
        print search.run()