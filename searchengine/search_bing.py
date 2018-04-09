# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'


from lib import myparser
from lib.log import logger
import time
from lib import myrequests
req = myrequests

class search_bing:

    def __init__(self, domain, limit, proxy=None):
        self.engine_name = "Bing"
        self.domain = domain.replace(' ', '%20')
        self.results = ""
        self.totalresults = ""
        self.url = "https://cn.bing.com/search"
        self.limit = int(limit)
        self.counter = 0
        self.headers = {"Cookie":"SRCHHPGUSR=ADLT=DEMOTE&NRSLT=50","Accept-Language":"'en-us,en"}
        self.proxies = proxy
        self.print_banner()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def do_search(self):
        url = "{0}?q=site:{1}&count=50&first={2}".format(self.url, self.domain, self.counter)  # 这里的pn参数是条目数
        r = req.get(url, headers = self.headers, proxies = self.proxies)
        self.results = r.content
        self.totalresults += self.results
        try:

            return True
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))
            return False

    def do_search_vhost(self):
        url = "{0}q=ip:{1}&go=&count=50&FORM=QBHL&qs=n&first={2}".format(self.url,self.ip,self.counter)

    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.domain)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.domain)
        return rawres.hostnames()

    def get_allhostnames(self):
        rawres = myparser.parser(self.totalresults, self.domain)
        return rawres.hostnames_all()

    def process(self):
        while (self.counter < self.limit):
            if self.do_search():
                #self.do_search_vhost()
                time.sleep(1)
                self.counter += 50
                continue
            else:
                break
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        logger.info("{0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e)))
        return self.d, self.e

if __name__ == "__main__":
        print "[-] Searching in Bing:"
        search = search_bing("meizu.com", '10')
        print search.run()