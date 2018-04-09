# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib.myparser import parser
from lib.log import logger
import time
import config
from lib import myrequests
req = myrequests

'''
#创建自定义的搜索引擎（CSE）获取cx参数即engine ID:   https://cse.google.com/cse/all
#申请API Key: https://developers.google.com/custom-search/json-api/v1/overview
#接口参数测试： https://developers.google.com/apis-explorer/?hl=en_US#p/customsearch/v1/search.cse.list
'''

class search_google_cse:
    def __init__(self, word, limit=100, proxy=None):
        self.engine_name = "Google_CSE"
        self.word = word
        self.files = "pdf"
        self.results = ""
        self.totalresults = ""
        self.url = "https://www.googleapis.com/customsearch/v1"
        self.quantity = "10"
        self.limit = int(limit)
        self.counter = 1 #不能是0,每一页的第一个内容的id
        self.timeout = 20
        try:
            self.api_key = config.Google_CSE_API_Key
            self.cse_id = config.Google_CSE_ID
        except:
            logger.error("No Google CSE API Key,Exit..")
            exit(0)
        self.lowRange = 0
        self.highRange = 100
        self.proxies = proxy
        self.print_banner()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def do_search(self):
        try:
            url = "{0}?key={1}&highRange={2}&lowRange={3}&cx={4}&start={5}&q={6}".format(self.url,self.api_key,self.highRange,self.lowRange,self.cse_id,self.counter,self.word)
            r = req.get(url, proxies=self.proxies, timeout=self.timeout,verify =False)
            #print r.content
            if r.status_code != 200:
                return False
            else:
                self.results = r.content
                self.totalresults += self.results
                return True
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return False

    def do_search_files(self):
        try:
            query = "filetype:"+self.files+"%20site:"+self.word
            url = "{0}?key={1}&highRange={2}&lowRange={3}&cx={4}&start={5}&q={6}".format(self.url,self.api_key,self.highRange,self.lowRange,self.cse_id,self.counter,query)
            r = req.get(url,proxies=self.proxies)
            if "and not a robot" in r.content:
                logger.warning("google has blocked your visit")
                return -1
            else:
                self.results = r.content
                self.totalresults += self.results
                return 1
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return -1

    def get_emails(self):
        rawres = parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = parser(self.totalresults, self.word)
        return rawres.hostnames()

    def get_files(self):
        rawres = parser(self.totalresults, self.word)
        return rawres.fileurls(self.files)

    def process(self):
        tracker = self.counter + self.lowRange
        while tracker <= self.limit:
            if self.do_search():
                # print "\tSearching " + str(self.counter+self.lowRange) + " results...\t\t\t\t\t\r"
                if self.counter == 101:
                    self.counter = 1
                    self.lowRange += 100
                    self.highRange += 100
                else:
                    self.counter += 10
                tracker = self.counter + self.lowRange
            else:
                break

    def store_results(self):
        filename = "debug_results.txt"
        file = open(filename, 'w')
        file.write(self.totalresults)

    def process_files(self, files):
        while self.counter <= self.limit:
            self.do_search_files(files)
            time.sleep(1)
            self.counter += 100
            #print "\tSearching " + str(self.counter) + " results..."
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        logger.info("{0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e)))
        return self.d, self.e

if __name__ == "__main__":
    proxy = {"http": "http://127.0.0.1:9988","https":"https://127.0.0.1:9988"}
    useragent = "Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"  # 他会检查useragent，之前多了一个( 导致504
    x = search_google_cse("meizu.com",100,proxy)
    print x.run()