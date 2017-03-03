__author__ = 'bit4'
#coding:utf-8
from search import search
import re
import multiprocessing
import threading


class baidu_search(search):
    def __init__(self, key_word=None, limit=1000, proxy=None):
        self.base_url = "http://www.baidu.com/s?wd=%40{query}&pn={page_no}"
        self.engine_name = "baidu"
        self.counter_step = 10  #item number,10 items each page
        self.proxy = None  # no proxy need for baidu
        search.__init__(self, self.base_url, self.engine_name, key_word, limit, self.proxy)

    def check_response_errors(self, resp):
        return False # baidu will not block our requset

class so_search(search):
    def __init__(self, key_word=None, limit=1000, proxy=None):
        self.base_url = "https://www.so.com/s?q={query}&pn={page_no}"
        self.engine_name = "so.com"
        self.counter_step = 1  #item number,10 items each page
        self.proxy = None  # no proxy need for baidu
        search.__init__(self, self.base_url, self.engine_name, key_word, limit, self.proxy)

    def check_response_errors(self, resp):
        return False # baidu will not block our requset

class ask_search(search):
    def __init__(self, key_word=None, limit=None, proxy=None):
        self.base_url = "http://www.ask.com/web?q={query}&pu=100&page={page_no}"
        self.engine_name = "ask"
        self.counter_step = 1 #page_no ,
        search.__init__(self, self.base_url, self.engine_name, key_word, limit, proxy) #need proxy
    def check_response_errors(self, resp):
        return False

    def check_next(self):
        renext = re.compile('>  Next  <')
        nextres = renext.findall(self.results)
        if nextres != []:
            nexty = "1"
        else:
            nexty = "0"
        return nexty


class bing_search(search):
    def __init__(self, key_word=None, limit=None, proxy=None):
        self.base_url = "http://cn.bing.com/search?q={query}&go=&count=50&FORM=QBHL&qs=n&first={page_no}"
        self.engine_name = "bing"
        self.counter_step = 50
        self.proxy = None
        search.__init__(self, self.base_url, self.engine_name, key_word, limit, self.proxy)
    def check_response_errors(self, resp):
        return False


class dogpile_search(search):
    def __init__(self, key_word=None, limit=None, proxy=None):
        self.base_url = "http://www.dogpile.com/search/web?q={query}&qsi={page_no}"
        self.engine_name = "dogpile"
        self.counter_step = 10
        search.__init__(self, self.base_url, self.engine_name, key_word, limit, proxy)
        self.proxy = None
    def check_response_errors(self, resp):
        return False



class exalead_search(search):
    def __init__(self, key_word=None, limit=None, proxy=None):
        self.base_url = "http://www.exalead.com/search/web/results/?q={query}&&elements_per_page=50&start_index=={page_no}"
        self.engine_name = "exalead"
        self.counter_step = 50
        search.__init__(self, self.base_url, self.engine_name, key_word, limit, proxy)
    def check_response_errors(self, resp):
        return False

    def check_next(self):
        renext = re.compile('topNextUrl')
        nextres = renext.findall(self.results)
        if nextres != []:
            nexty = "1"
            print str(self.counter)
        else:
            nexty = "0"
        return nexty


class google_search(search):
    def __init__(self, key_word=None, limit=None, proxy=None):
        self.base_url = "https://google.com/search?q={query}&btnG=Search&hl=en-US&biw=&bih=&gbv=1&start={page_no}&filter=0"
        self.engine_name = "google"
        self.counter_step = 10
        search.__init__(self, self.base_url, self.engine_name, key_word, limit, proxy)
        
    def check_response_errors(self, resp):
        if resp is None:
            pass
        elif 'Our systems have detected unusual traffic' in resp:
            print "[!] Error: Google probably now is blocking our request"
            return True
        return False # baidu will not block our requset


class yahoo_search(search):
    def __init__(self, key_word=None, limit=None, proxy=None):
        self.base_url = "http://search.yahoo.com//search?p={query}&b={page_no}&pz=10"
        self.engine_name = "yahoo"
        self.counter_step = 10
        self.proxy = None
        search.__init__(self, self.base_url, self.engine_name, key_word, limit, self.proxy)
        
    def check_response_errors(self, resp):
        if resp is None:
            pass
        elif 'Our systems have detected unusual traffic' in resp:
            print "[!] Error: Google probably now is blocking our requests"
            return True
        return False #

class yandex_search(search):
    def __init__(self, key_word=None, limit=None, proxy=None):
        self.base_url = "http://www.yandex.com/search?text={query}&numdoc=50&lr={page_no}"
        self.engine_name = "yandex"
        self.counter_step = 50
        self.proxy =None
        search.__init__(self, self.base_url, self.engine_name, key_word, limit, self.proxy)
        
    def check_response_errors(self, resp):
        if resp is None:
            pass
        elif "temporarily block your access" in resp:
            print "[!] Error: Yandex probably now is blocking our requests"
            return True
        return False
    def check_next(self):
        renext = re.compile('topNextUrl')
        nextres = renext.findall(self.results)
        if nextres != []:
            nexty = "1"
            print str(self.counter)
        else:
            nexty = "0"
        return nexty

def callengines(key_word,limit=1000,proxy=None):
    final_domains = []
    final_emails = []
    enums = [enum(key_word, limit, proxy) for enum in baidu_search, ask_search, bing_search, dogpile_search, exalead_search, google_search, yandex_search, yahoo_search]
    #enums = [enum(key_word, limit, proxy) for enum in baidu_search, ask_search]

    for enum in enums:
        domain, email = enum.run()
        final_domains.extend(domain)
        final_emails.extend(email)
    return list(set(final_domains)),list(set(final_emails))

def callengines_thread(engine,key_word,limit=1000,proxy=None):
    final_domains = []
    final_emails = []
    x = engine(key_word, limit, proxy)
    domain, email = x.run()
    if "2f" or "2F" in domain:
        print domain
        print engine
    print domain,email
    final_domains.extend(domain)
    final_emails.extend(email)

if __name__ == "__main__":
    proxy = {
    "http": "http://127.0.0.1:9999/",
    "https": "http://127.0.0.1:9999/",
    }
    Threadlist = []
    for engine in [baidu_search, so_search, ask_search, bing_search, dogpile_search, exalead_search, google_search, yandex_search, yahoo_search]:
        t = threading.Thread(target=callengines_thread,args=(engine,"meizu.com",100,proxy))
        Threadlist.append(t)
    for t in Threadlist:
        print t
    for t in Threadlist: #use start() ,not run()
        t.start()
    for p in Threadlist:
        t.join()





