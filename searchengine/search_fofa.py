# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import base64
import config
from lib import myparser
from lib.log import logger
from lib import myrequests
req = myrequests

class search_fofa:
    def __init__(self, word, limit,proxy=None):
        self.engine_name = "Fofa"
        try:
            self.email = config.FOFA_USER_EMAIL
            self.key = config.FOFA_API_KEY
        except:
            logger.warning("No Fofa Config,Exit")
            exit(0)
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.server = "fofa.so"
        self.limit = int(limit)
        self.counter = 0 #useless
        self.proxies = proxy
        self.print_banner()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return
    def do_search(self):
        try:
            auth_url = "https://fofa.so/api/v1/info/my?email={0}&key={1}".format(self.email, self.key)
            auth = req.get(auth_url)
            query = base64.b64encode("domain="+self.word)
            url = "https://fofa.so/api/v1/search/all?email={0}&key={1}&qbase64={2}".format(self.email, self.key,
                                                                                           query)
            r = req.get(url, proxies=self.proxies)
            self.results = r.content
            self.totalresults += self.results
            return True
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return False
    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()
    def process(self):
        self.do_search()
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        logger.info("{0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e)))
        return self.d, self.e

if __name__ == "__main__":
        print "[-] Searching in fofa:"
        useragent = "Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6" #他会检查useragent，之前多了一个( 导致504
        proxy = {"http": "http://127.0.0.1:8080"}
        search = search_fofa("meizu.com", 100, useragent)
        print search.run()