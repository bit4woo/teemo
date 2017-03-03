__author__ = 'bit4'
#coding:utf-8

#from wydomain
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
import threading
from multiprocessing import Queue


def callsites(key_word,proxy=None):
    final_domains = []
    final_emails = []
    enums = [enum(key_word, proxy) for enum in Alexa,Chaxunla,CrtSearch,DNSdumpster,Googlect,Ilink,Netcraft,PassiveDNS,Pgpsearch,Sitedossier,ThreatCrowd,Threatminer]
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
    "http": "http://127.0.0.1:9999/",
    "https": "http://127.0.0.1:9999/",
    }
    #print callsites("meizu.com",proxy="http://127.0.0.1:9999")
    Threadlist = []
    q = Queue()
    for engine in [Alexa,Chaxunla,CrtSearch,DNSdumpster,Googlect,Ilink,Netcraft,PassiveDNS,Pgpsearch,Sitedossier,ThreatCrowd,Threatminer]:
        #print callsites_thread(engine,"meizu.com",proxy)
        t = threading.Thread(target=callsites_thread,args=(engine,"meizu.com",q,proxy))
        Threadlist.append(t)
    for t in Threadlist:
        print t
    for t in Threadlist: # use start() not run()
        t.start()
    for p in Threadlist:
        t.join()
    print q