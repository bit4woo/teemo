from lib import myparser
import time
import requests
import random

class search(object):
    def __init__(self, base_url, engine_name, key_word, limit=1000, proxy=None):

        self.results = ""
        self.total_results = ""

        self.counter = 0
        self.counter_step = 10 #10 or 50
        self.limit = int(limit) #100*

        #self.session = requests.Session()
        self.timeout = 5
        self.base_url = base_url #"http://www.baidu.com/s?wd=%40{query}&pn={page_no}"
        self.engine_name = engine_name
        self.key_word = key_word
        self.proxy = proxy

    def do_search(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-GB,en;q=0.5',
                   'Accept-Encoding': 'gzip, deflate',
                   'Connection': 'keep-alive'
                   }
        url =  self.base_url.format(query=self.key_word, page_no=self.counter)
        #resp = requests.get(url, headers=headers, timeout=self.timeout, proxies=self.proxy)
        try:
            resp = requests.get(url, headers=headers, timeout=self.timeout, proxies=self.proxy)
        except Exception as e:
            print e
            return None
            pass
        if hasattr(resp, "text"):
            return resp.text
        else:
            return resp.content
    def check_next(self):
        """ chlid class should override this function"""
        return "1"
    #override
    def check_response_errors(self, resp):
        """ chlid class should override this function
        The function should return False if there are no errors and False otherwise
        """
        return True

    def process(self):
        print "[-] Searching now in %s" % self.engine_name
        while self.counter <= self.limit and self.counter <= 1000:
            self.result = self.do_search()
            if self.check_response_errors(self.result) or self.result== None:# None == requeset error
                break
            else:
                self.total_results += self.result
                time.sleep(random.randint(1, 3))
                #print "\tSearching " + str(self.counter) + " results in "+self.engine_name
                more = self.check_next()
                if more == "1":
                    self.counter += self.counter_step
                else:
                    break

    def get_emails(self):
        rawres = myparser.parser(self.total_results, self.key_word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.total_results, self.key_word)
        return rawres.hostnames()

    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        self.e = self.get_emails()
        print "[-] {0} found {1} domain(s) and {2} email(s)".format(self.engine_name,len(self.d),len(self.e))
        return self.d, self.e



######test########

class baidu_searchtest(search):
    def __init__(self, key_word=None, limit=None, proxy=None):
        self.base_url = "http://www.baidu.com/s?wd=%40{query}&pn={page_no}"
        self.engine_name = "baidu"
        self.counter_step = 10
        search.__init__(self, self.base_url, self.engine_name,key_word, limit, proxy)
    def check_response_errors(self, resp):
        return False # baidu will not block our requset



if __name__ == "__main__":
        search = baidu_searchtest("meizu.com", '10')
        print search.run()
