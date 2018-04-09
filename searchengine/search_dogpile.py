# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib import myparser
from lib.log import logger
import time
from lib import myrequests
req = myrequests

class search_dogpile:

    def __init__(self, word, limit, proxy=None):
        self.engine_name = "DogPile"
        self.word = word
        self.total_results = ""
        self.results =""
        self.server = "www.dogpile.com"
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
            url = "http://{0}/search/web?qsi={1}&q={2}".format(self.server,self.counter,self.word)
            r = req.get(url, proxies = self.proxies)
            self.results = r.content
            self.total_results += self.results
            return True
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return False


    def process(self):
        while self.counter <= self.limit and self.counter <= 1000:
            if self.do_search():
                time.sleep(1)
                #print "\tSearching " + str(self.counter) + " results..."
                self.counter += 20
                continue
            else:
                break

    def get_emails(self):
        rawres = myparser.parser(self.total_results, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.total_results, self.word)
        return rawres.hostnames()
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        logger.info("{0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e)))
        return self.d, self.e

if __name__ == "__main__":
        print "[-] Searching in dogpilesearch:"
        useragent = "Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6" #他会检查useragent，之前多了一个( 导致504
        proxy = {"http": "http://127.0.0.1:9988"}
        search = search_dogpile("meizu.com", '100',proxy)
        print search.run()