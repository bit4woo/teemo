import httplib
from lib import myparser
import time
import threading


class search_baidu:

    def __init__(self, word, limit, proxy=None):
        self.word = word
        self.limit = int(limit)
        self.total_results = ""
        self.proxy = proxy

        self.server = "www.baidu.com"
        self.hostname = "www.baidu.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.baseurl = "/s?wd=%40"
        self.counter = 0

    def do_search(self):
        h = httplib.HTTP(self.server)

        h.putrequest('GET', "/s?wd=%40" + self.word
                     + "&pn=" + str(self.counter))
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()

        self.total_results += h.getfile().read()

    def process(self):
        while self.counter <= self.limit and self.counter <= 1000:
            self.do_search()
            time.sleep(1)

            #print "\tSearching " + str(self.counter) + " results..."
            self.counter += 10

    def get_emails(self):
        rawres = myparser.parser(self.total_results, self.word)
        print "%s email(s) found in Baidu" %len(rawres.emails())
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.total_results, self.word)
        print "%s domain(s) found in Baidu" %len(rawres.hostnames())
        return rawres.hostnames()

def baidu(keyword, limit, proxy): #define this function to use in threading.Thread(),becuase the arg need to be a function
    search = search_baidu(keyword, limit)
    search.process()
    print search.get_emails()
    return search.get_emails(), search.get_hostnames()

if __name__ == "__main__":
        search = search_baidu("meizu.com", '1000')
        search.process()
        all_emails = search.get_emails()
        all_hosts = search.get_hostnames()
        print all_hosts
        print all_emails#test successed
