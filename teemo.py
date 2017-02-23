# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'

import os
import argparse
from multiprocessing import Queue
import socket
from lib.common import *
from subbrute import subbrute
import threading

from config import GoogleCSE_API_Key,default_proxies
import datetime


from searchengine.searchimpl import baidu_search,so_search, ask_search, bing_search, dogpile_search, exalead_search, google_search, yandex_search, yahoo_search

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


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#In case you cannot install some of the required development packages, there's also an option to disable the SSL warning:
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    pass

#Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')

# Console Colors
if is_windows:
    # Windows deserve coloring too :D
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white
    try:
        import win_unicode_console , colorama
        win_unicode_console.enable()
        colorama.init()
        #Now the unicode will work ^_^
    except:
        print("[!] Error: Coloring libraries not installed ,no coloring will be used [Check the readme]")
        G = Y = B = R = W = G = Y = B = R = W = ''


else:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white

version = 'V 0.1'

def banner():
    print """%s

          #####  ######  ######  #    #   ####
            #    #       #       ##  ##  #    #
            #    #####   #####   # ## #  #    #
            #    #       #       #    #  #    #
            #    #       #       #    #  #    #
            #    ######  ######  #    #   ####

            %s%s

         # Coded By bit4 - https://github.com/bit4woo
         # %s
  """ % (R, W, Y, version)

def parser_error(errmsg):
    banner()
    print "Usage: python "+sys.argv[0]+" [Options] use -h for help"
    print R+"Error: "+errmsg+W
    sys.exit()

def parse_args():
    #parse the arguments
    parser = argparse.ArgumentParser(epilog = '\tExample: \r\npython '+sys.argv[0]+" -d google.com")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--domain', help="Domain name to enumrate it's subdomains", required=True)
    parser.add_argument('-b', '--bruteforce', help='Enable the subbrute bruteforce module',nargs='?', default=False)
    parser.add_argument('-p', '--ports', help='Scan the found subdomains against specified tcp ports')
    #parser.add_argument('-v', '--verbose', help='Enable Verbosity and display results in realtime',nargs='?', default=False)
    #parser.add_argument('-t', '--threads', help='Number of threads to use for subbrute bruteforce', type=int, default=30)
    parser.add_argument('-o', '--output', help='Save the results to text file')
    parser.add_argument('-x', '--proxy', help='The http proxy to visit google')
    return parser.parse_args()

def write_file(filename, subdomains): #如何保证中文也争取
    #saving subdomains results to output file
    print "%s[-] Saving results to file: %s%s%s%s"%(Y,W,R,filename,W)
    with open(str(filename), 'wb') as f:
        for subdomain in subdomains:
            f.write(subdomain+"\r\n")

class portscan():

    def __init__(self,subdomains,ports):
        self.subdomains = subdomains
        self.ports = ports
        self.threads = 20
        self.lock = threading.BoundedSemaphore(value=self.threads)

    def port_scan(self,host,ports):
        openports = []
        self.lock.acquire()
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result = s.connect_ex((host, int(port)))
                if result == 0:
                    openports.append(port)
                s.close
            except Exception as e:
                pass
        self.lock.release()
        if len(openports) > 0:
            print "%s%s%s - %sFound open ports:%s %s%s%s"%(G,host,W,R,W,Y,', '.join(openports),W)

    def run(self):
        for subdomain in self.subdomains:
            t = threading.Thread(target=self.port_scan,args=(subdomain,self.ports))
            t.start()


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
    domains = enum.run()
    if domains:
        for domain in domains:
            q_domains.put(domain)
        #return list(set(final_domains))



def main():
    args = parse_args()
    domain = args.domain
    #threads = args.threads
    savefile = args.output
    ports = args.ports
    bruteforce_list = []
    subdomains = []

    if not savefile:
        now = datetime.datetime.now()
        timestr = now.strftime("-%Y-%m-%d-%H-%M")
        savefile = domain+timestr+".txt"

    if args.proxy != None:
        proxy = args.proxy
        proxy = {args.proxy.split(":")[0]: proxy}
    elif default_proxies != None:  #config.py
        proxy = default_proxies
    else:
        proxy = {}

    #Check Verbosity
    #global verbose
    #verbose = args.verbose
    #if verbose or verbose is None:
        #verbose = True

    #Check Bruteforce Status
    enable_bruteforce = args.bruteforce
    if enable_bruteforce or enable_bruteforce is None:
        enable_bruteforce = True

    #Validate domain
    if not is_domain(domain):
        print R+"Error: Please enter a valid domain"+W
        sys.exit()


    #Print the Banner
    banner()
    waring = "[!] legal disclaimer: Usage of Teemo for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program"
    print waring
    print B+"[-] Enumerating subdomains now for %s"% domain+W

    '''
    subdomains.extend(callsites(domain,proxy))
    domains,emails = callengines(domain,500,proxy)
    subdomains.extend(domains)
    #print subdomains
    '''

    Threadlist = []
    q_domains = Queue() #to recevie return values
    q_emails = Queue()
    for engine in [Alexa, Chaxunla, CrtSearch, DNSdumpster, Googlect, Ilink, Netcraft, PassiveDNS, Pgpsearch, Sitedossier, ThreatCrowd, Threatminer]:
        #print callsites_thread(engine,domain,proxy)
        t = threading.Thread(target=callsites_thread, args=(engine, domain, q_domains, q_emails, proxy))
        Threadlist.append(t)
    for engine in [baidu_search, so_search, ask_search, bing_search, dogpile_search, exalead_search, google_search, yandex_search, yahoo_search]:
        t = threading.Thread(target=callengines_thread, args=(engine, domain, q_domains, q_emails, proxy, 500))
        Threadlist.append(t)
    #for t in Threadlist:
    #    print t
    for t in Threadlist: # use start() not run()
        t.start()
    for t in Threadlist:
        t.join()

    while not q_domains.empty():
        subdomains.append(q_domains.get())
    emails = []
    while not q_emails.empty():
        emails.append(q_emails.get())


    if enable_bruteforce:
        print G+"[-] Starting bruteforce module now using subDomainsBrute.."+W
        record_type = False
        path_to_file = os.path.dirname(os.path.realpath(__file__))
        subs = os.path.join(path_to_file, 'subbrute', 'names.txt')
        resolvers = os.path.join(path_to_file, 'subbrute', 'resolvers.txt')
        process_count = 10
        output = False
        json_output = False
        bruteforce_list = subbrute.print_target(domain, record_type, subs, resolvers, process_count, output, json_output, subdomains)
        subdomains.extend(bruteforce_list)


    if subdomains is not None:
        subdomains = sorted(list(set(subdomains)))
        emails = sorted(list(set(emails)))
        subdomains.extend(emails) #this function return value is NoneType ,can't use in function directly
        #print type(subdomains)

        write_file(savefile, subdomains)

        if ports:
            print G+"[-] Start port scan now for the following ports: %s%s"%(Y,ports)+W
            ports = ports.split(',') #list
            pscan = portscan(subdomains,ports)
            pscan.run()

        else:
            for subdomain in subdomains:
                print G+subdomain+W

    print "[+] {0} domains found in total".format(len(subdomains))
    print "[+] {0} emails found in total".format(len(emails))
    print "[+] Results saved to {0} in {1}".format(savefile,os.getcwd())

if __name__=="__main__":
    main()
