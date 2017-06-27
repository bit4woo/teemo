# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
from lib import myparser
import time
import requests
#


class search_google():

    def __init__(self, word, limit, start, proxy):
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.server = "www.google.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.quantity = "100"
        self.limit = limit
        self.counter = start
        self.proxies = proxy
    def do_search(self):
        try:
            urly = "http://" + self.server + "/search?num=" + self.quantity + "&start=" + str(self.counter) + "&hl=en&meta=&q=%40\"" + self.word + "\""
        except Exception, e:
            print e
        try:
            r = requests.get(urly, proxies=self.proxies)
            if "and not a robot" in r.content:
                print "google has blocked your visit"
                return 0
            else:
                self.results = r.content
                self.totalresults += self.results
                return 1
        except Exception,e:
            print e
            return 0

    def do_search_profiles(self):
        try:
            urly="http://" + self.server + "/search?num=" + self.quantity + "&start=" + str(self.counter) + "&hl=en&meta=&q=site:www.google.com%20intitle:\"Google%20Profile\"%20\"Companies%20I%27ve%20worked%20for\"%20\"at%20" + self.word + "\""
        except Exception, e:
            print e
        try:
            r=requests.get(urly, proxies=self.proxies)
        except Exception,e:
            print e
        self.results = r.content

        #'&hl=en&meta=&q=site:www.google.com%20intitle:"Google%20Profile"%20"Companies%20I%27ve%20worked%20for"%20"at%20' + self.word + '"')
        self.totalresults += self.results

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
            if self.do_search() == 0:
                break
            #more = self.check_next()
            time.sleep(1) #should to sleep random time and use random user-agent to prevent block
            print "\tSearching " + str(self.counter) + " results..."
            self.counter += 100

    def process_profiles(self):
        while self.counter < self.limit:
            self.do_search_profiles()
            time.sleep(0.3)
            self.counter += 100
            print "\tSearching " + str(self.counter) + " results..."


if __name__ == "__main__":
        print "[-] Searching in Google:"
        proxy = {"http":"http://127.0.0.1:9999"}
        search = search_google("meizu.com", '1000', 0, proxy)
        search.process()
        all_emails = search.get_emails()
        all_hosts = search.get_hostnames()
        print all_emails
        print all_hosts #ip blocked