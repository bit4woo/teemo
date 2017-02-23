from lib import myparser
import re
import requests


class search_ask():

    def __init__(self, word, limit, proxy):
        self.word = word.replace(' ', '%20')
        self.results = ""
        self.totalresults = ""
        self.server = "www.ask.com"
        self.hostname = "www.ask.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.quantity = "100"
        self.limit = int(limit)
        self.counter = 0
        self.proxies = proxy

    def do_search(self):
        '''
        h = httplib.HTTP(self.server)
        h.putrequest(
            'GET',
            "/web?q=%40{0}&pu=100&page={1}".format(self.word,self.counter))
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()
        self.results = h.getfile().read()
        self.totalresults += self.results
        '''

        try:
            urly = "http://{0}/web?q={1}&pu=100&page={2}".format(self.server,self.word,self.counter)
        except Exception, e:
            print e
        try:
            r = requests.get(urly, proxies = self.proxies)
            self.results = r.content
            self.totalresults += self.results
        except Exception,e:
            print e


    def check_next(self):
        renext = re.compile('>  Next  <')
        nextres = renext.findall(self.results)
        if nextres != []:
            nexty = "1"
        else:
            nexty = "0"
        return nexty

    def get_people(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.people_jigsaw()

    def process(self):
        while (self.counter < self.limit):
            self.do_search()
            more = self.check_next()
            if more == "1":
                self.counter += 1
            else:
                break
    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()

def ask(keyword, limit, proxy): #define this function to use in threading.Thread(),becuase the arg need to be a function
    search = search_ask(keyword, limit, proxy)
    search.process()
    print search.get_emails()
    return search.get_emails(), search.get_hostnames()




if __name__ == "__main__":
    proxy = {"http":"http://127.0.0.1:9999"}
    search = search_ask("meizu.com", '1000', proxy)
    search.process()
    emails = search.get_emails()
    hosts = search.get_hostnames()
    print emails
    print hosts #test successed