# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
import requests
from lib import myparser
import time
import config

class search_duckduckgo:

    def __init__(self, word, limit, useragent, proxy=None):
        self.engine_name = "DuckDuckGo"
        self.word = word
        self.total_results = ""
        self.results =""
        self.server = "duckduckgo.com" #https://duckduckgo.com/
        self.limit = int(limit)
        self.counter = 0
        self.headers = {
            'User-Agent': useragent}
        self.proxies = proxy

    def do_search(self):
        try:
            url = "https://{0}/?q={1}".format(self.server,self.word)
        except Exception, e:
            print e
        try:
            r = requests.get(url, headers = self.headers, proxies = self.proxies)
            self.results = r.content
            self.total_results += self.results
        except Exception,e:
            print e

    def process(self):
        '''
        while self.counter <= self.limit and self.counter <= 1000:
            self.do_search()
            time.sleep(1)
            #print "\tSearching " + str(self.counter) + " results..."
            self.counter += 20
        '''
        self.do_search()
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
        print "[-] {0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e))
        return self.d, self.e

def dogpile(keyword, limit, useragent,proxy): #define this function to use in threading.Thread(),becuase the arg need to be a function
    search = search_duckduckgo(keyword, limit,useragent,proxy)
    search.process()
    print search.get_emails()
    return search.get_emails(), search.get_hostnames()


if __name__ == "__main__":
        print "[-] Searching in duckduckgo:"
        useragent = "Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6" #他会检查useragent，之前多了一个( 导致504
        proxy = {"http": "http://127.0.0.1:8080"}
        search = search_dogpile("meizu.com", '100',useragent,proxy)
        search.process()
        all_emails = search.get_emails()
        all_hosts = search.get_hostnames()
        print all_emails
        print all_hosts  # test pass