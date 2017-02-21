import httplib
import sys
import myparser
import time
from config import *


class search_bing:

    def __init__(self, word, limit, start):
        self.word = word.replace(' ', '%20')
        self.results = ""
        self.totalresults = ""
        self.apiserver = "api.search.live.net"
        self.hostname = "www.bing.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.quantity = "50"
        self.limit = int(limit)
        self.bingApi = bing_API_key
        self.counter = start

    def do_search_api(self):
        h = httplib.HTTP(self.apiserver)
        h.putrequest('GET', "/xml.aspx?Appid=" + self.bingApi + "&query=%40" +
                     self.word + "&sources=web&web.count=40&web.offset=" + str(self.counter))
        h.putheader('Host', "api.search.live.net")
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()
        self.results = h.getfile().read()
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

    def process(self, bingApi):
        if self.bingApi != "":
            while (self.counter < self.limit):
                self.do_search_api()
                time.sleep(0.3)
                self.counter += 50
            print "\tSearching " + str(self.counter) + " results..."
        else:
            print "Please insert your API key in the discovery/bingsearch.py"
            sys.exit()


if __name__ == "__main__":
        print "[-] Searching in Bing:"
        search = search_bing("meizu.com", '100', 0)
        search.process('yes')
        all_emails = search.get_emails()
        all_hosts = search.get_hostnames()
        print all_emails
        print all_hosts  # officcal service stopped ?