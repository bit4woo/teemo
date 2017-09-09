# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from domainsites.Alexa import Alexa
from domainsites.Chaxunla import Chaxunla
from domainsites.CrtSearch import CrtSearch
from domainsites.DNSdumpster import DNSdumpster
from domainsites.Googlect import Googlect
from domainsites.Ilink import Ilink
from domainsites.Netcraft import Netcraft
from domainsites.PassiveDNS import PassiveDNS
from domainsites.Pgpsearch import Pgpsearch
from domainsites.Sitedossier import Sitedossier
from domainsites.ThreatCrowd import ThreatCrowd
from domainsites.Threatminer import Threatminer
from domainsites.Virustotal import Virustotal
import threading
from multiprocessing import Queue


def callsites(key_word,proxy=None):
    final_domains = []
    final_emails = []
    enums = [enum(key_word, proxy) for enum in Alexa,Chaxunla,CrtSearch,DNSdumpster,Googlect,Ilink,Netcraft,PassiveDNS,Pgpsearch,Sitedossier,ThreatCrowd,Threatminer,Virustotal]
    for enum in enums:
        domain = enum.run()
        final_domains.extend(domain)
        #final_emails.extend(email)
    return list(set(final_domains))


def callsites_thread(engine,key_word, q, proxy=None,):
    enum = engine(key_word,proxy)
    domain = enum.run()
    #final_emails.extend(email)
    for item in list(set(domain)):
        q.put(item)

if __name__ == "__main__":
    proxy = {
    "http": "http://127.0.0.1:9988/",
    "https": "http://127.0.0.1:9988/",
    }
    #print callsites("meizu.com",proxy="http://127.0.0.1:9999")
    Threadlist = []
    q = Queue()
    for engine in [Alexa,Chaxunla,CrtSearch,DNSdumpster,Googlect,Ilink,Netcraft,PassiveDNS,Pgpsearch,Sitedossier,ThreatCrowd,Threatminer,Virustotal]:
        #print callsites_thread(engine,"meizu.com",proxy)
        t = threading.Thread(target=callsites_thread,args=(engine,"meizu.com",q,proxy))
        Threadlist.append(t)

    for t in Threadlist: # use start() not run()
        t.start()
        t.join
    print q