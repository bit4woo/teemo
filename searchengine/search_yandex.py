# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
import httplib
from lib import myparser
from lib.log import logger
import re
import time
import requests
import random

class search_yandex:

    def __init__(self, word, limit, useragent, proxy=None):
        self.engine_name = "Yandex"
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.server = "yandex.com"
        self.hostname = "yandex.com"
        self.headers = {
            'User-Agent': useragent}
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
            url = "http://{0}/search?text={1}&numdoc=50&lr={2}".format(self.server,self.word,self.counter) #  %40=@ 搜索内容如：@meizu.com;在关键词前加@有何效果呢？，测试未发现不同
        except Exception, e:
            logger.error(e)
        try:
            r = requests.get(url, headers = self.headers, proxies = self.proxies)
            if "automated requests" in r.content:
                logger.warning("yandex blocked our request.exit")
                exit(0)
            self.results = r.content
            self.totalresults += self.results
        except Exception,e:
            logger.error(e)

    def do_search_files(self, files):  # TODO
        h = httplib.HTTP(self.server)
        h.putrequest('GET', "/search?text=%40" + self.word +
                     "&numdoc=50&lr=" + str(self.counter))
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()
        self.results = h.getfile().read()
        self.totalresults += self.results

    def check_next(self):
        renext = re.compile('topNextUrl')
        nextres = renext.findall(self.results)
        if nextres != []:
            nexty = "1"
            #print str(self.counter)
        else:
            nexty = "0"
        return nexty

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
            self.do_search()
            time.sleep(random.randint(1,5))
            self.counter += 50
            #print "Searching " + str(self.counter) + " results..."

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
        proxy = {"http": "http://127.0.0.1:8080"}
        search = search_yandex("meizu.com", 10, useragent, proxy)
        search.process()
        all_emails = search.get_emails()
        all_hosts = search.get_hostnames()
        print all_emails
        print all_hosts