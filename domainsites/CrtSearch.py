# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import multiprocessing
import threading
import urlparse
import requests
import re
from lib.myparser import parser

class CrtSearch(multiprocessing.Process):
    def __init__(self, domain, proxy=None):

        self.base_url = 'https://crt.sh/?q=%25.{domain}'
        #self.domain = urlparse.urlparse(domain).netloc
        self.resp = ""
        self.domain = domain
        self.subdomains = []
        self.session = requests.Session()
        self.engine_name = "crt.sh"
        self.q = []
        self.timeout = 25
        self.print_banner()
        return

    def print_banner(self):
        print "[-] Searching now in %s.." %(self.engine_name)
        return


    def req(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        }

        try:
            resp = self.session.get(url, headers=headers, timeout=self.timeout)
            if hasattr(resp, "text"):
                return resp.text
            else:
                return resp.content
        except Exception as e:
            print e
            return 0


    def run(self):
        url = self.base_url.format(domain=self.domain)
        #print url
        self.resp = self.req(url)
        if self.resp:
            self.subdomains = self.get_hostnames()
        for domain in self.subdomains:
            self.q.append(domain)
        print "[-] {0} found {1} domains".format(self.engine_name, len(self.q))
        return self.q

    def get_hostnames(self):
        rawres = parser(self.resp, self.domain)
        return rawres.hostnames()

if __name__ == "__main__":
    x= CrtSearch("meizu.com")
    print x.run()