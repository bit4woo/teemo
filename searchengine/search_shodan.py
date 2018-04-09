# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'


import shodan
import config
from lib import myparser
from lib.log import logger
#
class search_shodan:
    def __init__(self, word, limit, useragent, proxy=None):
        self.engine_name = "Shodan"
        self.word = word.replace(' ', '%20')
        self.results = ""  # 本页搜索结果
        self.totalresults = ""  # 所有搜索结果
        self.server = "shodan.io"
        self.headers = {
                'User-Agent': useragent}
        self.limit = int(limit)
        self.counter = 0
        self.proxies = proxy
        try:
            self.apikey = config.SHODAN_API_KEY
        except:
            print "No Shodan API Key,Exit"
            exit(0)
        self.print_banner()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def do_search(self):
        try:
                api = shodan.Shodan(self.apikey)
                self.results = api.search(self.word)
                self.totalresults +=str(self.results)
                return True
        except shodan.APIError, e:
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
    proxy = {"http": "http://127.0.0.1:8080"}
    useragent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
    search = search_shodan("meizu.com",100, useragent)
    print search.run()