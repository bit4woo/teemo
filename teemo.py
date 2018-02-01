# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import argparse
import datetime
import os
import threading
import Queue

from brute.subDomainsBrute import SubNameBrute

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
from lib.common import *
from lib.domain2ip import domains2ips,iprange
from lib.colorlog import *
from lib.zonetransfer import zonetransfer
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

reload(sys)
sys.setdefaultencoding('utf-8')
sys.dont_write_bytecode = True


#In case you cannot install some of the required development packages, there's also an option to disable the SSL warning:
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    pass


def parser_error(errmsg):
    banner()
    print ("Usage: python "+sys.argv[0]+" [Options] use -h for help")
    logger.error("Error: "+errmsg)
    sys.exit()

def parse_args(): #optparse模块从2.7开始废弃，建议使用argparse
    parser = argparse.ArgumentParser(epilog = '\tExample: \r\npython '+sys.argv[0]+" -d google.com")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--domain', help="Domain name to enumrate it's subdomains", required=True)
    parser.add_argument('-b', '--bruteforce', help='Enable the subbrute bruteforce module',nargs='?', default=False)
    parser.add_argument('-o', '--output', help='Save the results to text file')
    parser.add_argument('-x', '--proxy', help='The http proxy to visit google,eg: http://127.0.0.1:8080 ')
    return parser.parse_args()

def adjust_args():
    args = parse_args()
    # Validate domain
    if not is_domain(args.domain):
        logger.error("Please enter a valid domain!!!")
        sys.exit()

    if not args.output:
        now = datetime.datetime.now()
        timestr = now.strftime("-%Y-%m-%d-%H-%M")
        args.output = args.domain + timestr + ".txt"
    args.output = os.path.join(os.path.dirname(__file__), "output", args.output)

    if args.proxy != None:
        proxy = {args.proxy.split(":")[0]: args.proxy}
    elif default_proxies != None and (proxy_switch == 2 or proxy_switch == 1):  # config.py
        proxy = default_proxies
    else:
        proxy = {}

    args.proxy = proxy_verify(proxy)
    if len(args.proxy) !=0:
        logger.info("Vailid Proxy: {0}".format(args.proxy))
    else:
        logger.info("Caution! No valid proxy detected. No proxy will be used in this run.")
    return args

def callengines_thread(engine, key_word, q_domains, q_emails, proxy=None,limit=1000):
    x = engine(key_word, limit, proxy)
    domains,emails = x.run()
    if domains: # domains maybe None
        for domain in domains:
            q_domains.put(domain)
    if emails:
        for email in emails:
            q_emails.put(email)

def callsites_thread(engine, key_word, q_domains, q_emails, proxy=None):
    enum = engine(key_word,proxy)
    domains,similar_domains,emails = enum.run()
    if domains:
        for domain in domains:
            q_domains.put(domain)
    if similar_domains:
        for item in  similar_domains:
            q_domains.put(item) #put both domain and similar in domain set
    if emails:
        for item in emails:
            q_emails.put(item)
        #return list(set(final_domains))

def main():
    try:
        banner()
        args = adjust_args()
        subdomains = []
        print "[-] Enumerating subdomains now for %s" % args.domain

        #doing zone transfer checking
        zonetransfer(args.domain).check()

        Threadlist = []
        q_domains = Queue.Queue() #to recevie return values,use it to ensure thread safe.
        q_emails = Queue.Queue()


        for engine in [Alexa, Chaxunla, CrtSearch, DNSdumpster, Googlect, Ilink, Netcraft, PassiveDNS, Pgpsearch, Sitedossier, ThreatCrowd, Threatminer,Virustotal]:
            #print callsites_thread(engine,domain,proxy)
            if proxy_switch == 1 and engine in proxy_default_enabled:
                pass
            else:
                proxy ={}
            t = threading.Thread(target=callsites_thread, args=(engine, args.domain, q_domains, q_emails, args.proxy))
            Threadlist.append(t)

        for engine in [search_ask,search_baidu,search_bing,search_bing_api,search_dogpile,search_duckduckgo,search_exalead,search_fofa,search_google,search_google_cse,
                       search_shodan,search_so,search_yahoo,search_yandex]:
            if proxy_switch == 1 and engine in proxy_default_enabled:
                pass
            else:
                proxy ={}
            t = threading.Thread(target=callengines_thread, args=(engine, args.domain, q_domains, q_emails, proxy, 500))
            t.setDaemon(True) #变成守护进程，独立于主进程。这里好像不需要
            Threadlist.append(t)

        #for t in Threadlist:
        #    print t
        for t in Threadlist: # use start() not run()
            t.start()
        for t in Threadlist: #为什么需要2次循环，不能在一次循环中完成？
            t.join() #主线程将等待这个线程，直到这个线程运行结束

        while not q_domains.empty():
            subdomains.append(q_domains.get())
        emails = []
        while not q_emails.empty():
            emails.append(q_emails.get())


        if args.bruteforce:
            print G+"[-] Starting bruteforce using subDomainsBrute.."+W
            d = SubNameBrute(target=args.domain)
            d.run()
            brute_lines = d.result_lines
            brute_domains = d.result_domains
            brute_ips = d.result_ips
        else:
            brute_ips = []
            brute_lines = []
            brute_domains = []


        if subdomains is not None: #prepaire output
            IP_list, lines = domains2ips(subdomains) #query domains that got from website and search engine

            IP_list.extend(brute_ips)
            IPrange_list = iprange(IP_list)

            subdomains.extend(brute_domains)
            subdomains = sorted(list(set(subdomains)))
            subdomain_number = len(subdomains)

            lines.extend(brute_lines)
            lines = list(set(lines))

            emails = sorted(list(set(emails)))

            subdomains.extend(emails) #this function return value is NoneType ,can't use in function directly
            subdomains.extend(IPrange_list)
            #print type(subdomains)
            for subdomain in subdomains:
                print G+subdomain+W

            subdomains.extend(lines)
            fp = open(args.output,"wb")
            #fp.writelines("\n".join(subdomains).decode("utf-8"))
            fp.writelines("\n".join(subdomains).encode("utf-8"))


        print "[+] {0} domains found in total".format(subdomain_number)
        print "[+] {0} emails found in total".format(len(emails))
        print "[+] Results saved to {0}".format(args.output)
    except KeyboardInterrupt as e:
        logger.info("Exit. Due To KeyboardInterrupt")


if __name__=="__main__":
    main()
