# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib import myparser
from lib.log import logger
import time
import random
from lib import myrequests
req = myrequests

class search_google():

    def __init__(self, word, limit, proxy=None):
        self.engine_name = "Google"
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.files = "pdf"
        self.url = "https://www.google.com/search"
        self.quantity = "100"
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
            url = "{0}?num={1}&start={2}&hl=en&meta=&q=site:{3}".format(self.url,self.quantity,self.counter,self.word)
            r = req.get(url, proxies=self.proxies)
            if "and not a robot" in r.content:
                logger.warning("Google has blocked your visit")
                return False
            else:
                self.results = r.content
                self.totalresults += self.results
                return True
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return False

    def do_search_profiles(self):
        try:
            urly="https://" + self.url + "/search?num=" + self.quantity + "&start=" + str(self.counter) + "&hl=en&meta=&q=site:www.google.com%20intitle:\"Google%20Profile\"%20\"Companies%20I%27ve%20worked%20for\"%20\"at%20" + self.word + "\""
            r = req.get(urly, proxies=self.proxies)
            self.results = r.content
            self.totalresults += self.results
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))


    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()

    def get_files(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.fileurls(self.files)

    def get_profiles(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.profiles()

    def process(self):
        while self.counter <= self.limit and self.counter <= 1000:
            if self.do_search():
                time.sleep(random.randint(1, 5))  # should to sleep random time and use random user-agent to prevent block
                self.counter += 100
            else:
                break

    def process_profiles(self):
        while self.counter < self.limit:
            self.do_search_profiles()
            time.sleep(0.3)
            self.counter += 100
            #print "\tSearching " + str(self.counter) + " results..."
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        logger.info("{0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e)))
        return self.d, self.e

if __name__ == "__main__":
        print "[-] Searching in Google:"
        proxy = {"https":"https://127.0.0.1:9988","http":"http://127.0.0.1:9988"}
        useragent = "Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"  # 他会检查useragent，之前多了一个( 导致504
        search = search_google("meizu.com", 100, proxy)
        print search.run()