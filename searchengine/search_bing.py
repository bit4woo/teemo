# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
import httplib
from lib import myparser
from lib.log import logger
import time
import requests

class search_bing:

    def __init__(self, word, limit, proxy=None):
        self.engine_name = "Bing"
        self.word = word.replace(' ', '%20')
        self.results = ""
        self.totalresults = ""
        self.server = "cn.bing.com"
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
        try:
            url = "http://{0}/search?q={1}&count=50&first={2}".format(self.server,self.word,self.counter)# 这里的pn参数是条目数
            r = requests.get(url, headers = self.headers, proxies = self.proxies)
            self.results = r.content
            self.totalresults += self.results
            return True
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))
            return False

    def do_search_vhost(self):
        h = httplib.HTTP(self.server)
        h.putrequest('GET', "/search?q=ip:" + self.word +
                     "&go=&count=50&FORM=QBHL&qs=n&first=" + str(self.counter))
        h.putheader('Host', self.hostname)
        h.putheader(
            'Cookie', 'mkt=en-US;ui=en-US;SRCHHPGUSR=NEWWND=0&ADLT=DEMOTE&NRSLT=50')
        h.putheader('Accept-Language', 'en-us,en')
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()
        self.results = h.getfile().read()
        #print self.results
        self.totalresults += self.results

    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()

    def get_allhostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
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
        useragent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        search = search_bing("meizu.com", '10', useragent)
        search.process()
        all_emails = search.get_emails()
        all_hosts = search.get_hostnames()
        print all_emails
        print all_hosts # test pass