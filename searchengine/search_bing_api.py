# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
import requests
from lib.log import logger
from lib import myparser
import time
import config


#https://azure.microsoft.com/zh-cn/try/cognitive-services/my-apis/
#https://api.cognitive.microsoft.com/bing/v5.0/search

#https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/quick-start

#https://api.cognitive.microsoft.com/bing/v5.0/search[?q][&count][&offset][&mkt][&safesearch]
#https://dev.cognitive.microsoft.com/docs/services/56b43eeccf5ff8098cef3807/operations/56b4447dcf5ff8098cef380d


class search_bing_api:

    def __init__(self, word, limit, useragent, proxy=None):
        self.engine_name = "BingAPI"
        self.word = word.replace(' ', '%20')
        self.results = ""
        self.totalresults = ""
        self.server = "api.cognitive.microsoft.com"
        self.headers = {'User-Agent': useragent,"Ocp-Apim-Subscription-Key":config.Bing_API_Key,}
        self.limit = int(limit)
        try:
            self.bingApikey = config.Bing_API_Key
        except:
            logger.warning("No Bing API Key,Exit")
            exit(0)
        self.counter = 0
        self.proxies = proxy
        self.print_banner()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def do_search(self):
        try:
            url = "http://api.cognitive.microsoft.com/bing/v5.0/search?q={0}&mkt=en-us".format(self.word,self.counter)# 这里的pn参数是条目数
        except Exception, e:
            logger.error(e)
        try:
            r = requests.get(url, headers = self.headers, proxies = self.proxies)
            self.results = r.content
            self.totalresults += self.results
        except Exception,e:
            logger.error(e)

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
            time.sleep(0.3)
            self.counter += 50
        #print "\tSearching " + str(self.counter) + " results..."


    def run(self):  # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        logger.info("{0} found {1} domain(s) and {2} email(s)".format(self.engine_name, len(self.d), len(self.e)))
        return self.d, self.e

def bing_API(keyword, limit, useragent, proxy): #define this function to use in threading.Thread(),becuase the arg need to be a function
    search = search_bing_api(keyword, limit, useragent, proxy)
    search.process()
    print search.get_emails()
    return search.get_emails(), search.get_hostnames()

if __name__ == "__main__":
        print "[-] Searching in Bing API:"
        useragent = "Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        proxy = {"http": "http://127.0.0.1:8080"}
        search = search_bing_api("meizu.com", '100', useragent, proxy)
        search.process()
        all_emails = search.get_emails()
        all_hosts = search.get_hostnames()
        print all_emails
        print all_hosts  # officcal service stopped ?