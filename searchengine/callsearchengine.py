# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from searchengine.search_ask import search_ask
from searchengine.search_baidu import search_baidu
from searchengine.search_bing import search_bing
from searchengine.search_bing_api import search_bing_api
from searchengine.search_dogpile import search_dogpile
from searchengine.search_duckduckgo import search_duckduckgo
from searchengine.search_exalead import search_exalead
from searchengine.search_fofa import search_fofa
from searchengine.search_google import search_google
from searchengine.search_google_cse import search_google_cse
from searchengine.search_shodan import search_shodan
from searchengine.search_so import search_so
from searchengine.search_yahoo import search_yahoo
from searchengine.search_yandex import search_yandex
import threading
from multiprocessing import Queue


def callengines_thread(engine, key_word, q_domains, q_emails, useragent, proxy=None,limit=1000):
    x = engine(key_word, limit, useragent, proxy)
    domains,emails = x.run()
    if domains: # domains maybe None
        for domain in domains:
            q_domains.put(domain)
    if emails:
        for email in emails:
            q_emails.put(email)

if __name__ == "__main__":
    proxy = {
    "http": "http://127.0.0.1:9988/",
    "https": "http://127.0.0.1:9988/",
    }
    #print callsites("meizu.com",proxy="http://127.0.0.1:9999")
    Threadlist = []
    q = Queue()
    q1= Queue()
    useragent = "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
    for engine in [search_ask,search_baidu,search_bing,search_bing_api,search_dogpile,search_duckduckgo,search_exalead,search_fofa,search_google,search_google_cse,
                   search_shodan,search_so,search_yahoo,search_yandex]:
        #print callsites_thread(engine,"meizu.com",proxy)
        t = threading.Thread(target=callengines_thread,args=(engine,"meizu.com",q,q1,useragent,proxy))
        Threadlist.append(t)

    for t in Threadlist: # use start() not run()
        t.start()
        t.join
    print q