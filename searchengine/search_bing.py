# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
import httplib
import sys
from lib import myparser
import time
from config import *


class search_bing:

    def __init__(self, word, limit):
        self.word = word.replace(' ', '%20')
        self.results = ""
        self.totalresults = ""
        self.server = "cn.bing.com"
        self.hostname = "cn.bing.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.quantity = "50"
        self.limit = int(limit)
        self.counter = 0

    def do_search(self):
        h = httplib.HTTP(self.server)
        h.putrequest('GET', "/search?q=%40" + self.word +
                     "&count=50&first=" + str(self.counter))
        h.putheader('Host', self.hostname)
        h.putheader('Cookie', 'SRCHHPGUSR=ADLT=DEMOTE&NRSLT=50')
        h.putheader('Accept-Language', 'en-us,en')
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()
        self.results = h.getfile().read()
        #print self.results
        self.totalresults += self.results

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
            self.do_search()
            self.do_search_vhost()
            time.sleep(1)
            self.counter += 50
            print "\tSearching " + str(self.counter) + " results..."


def bing(keyword, limit, proxy): #define this function to use in threading.Thread(),becuase the arg need to be a function
    search = search_bing(keyword, limit)
    search.process()
    print search.get_emails()
    return search.get_emails(), search.get_hostnames()

if __name__ == "__main__":
        print "[-] Searching in Bing:"
        search = search_bing("meizu.com", '10')
        search.process()
        all_emails = search.get_emails()
        all_hosts = search.get_hostnames()
        print all_emails
        print all_hosts # test pass