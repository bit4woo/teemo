# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

#this can search email address ,but not returned
from lib import myparser
from lib.log import logger
from lib import myrequests
req = myrequests

class PassiveDNS():
    def __init__(self, domain, proxy=None):
        self.proxy = proxy
        self.base_url = 'http://ptrarchive.com/tools/search.htm?label={domain}'
        self.domain = domain
        self.subdomains = []
        self.engine_name = "PassiveDNS"
        self.domain_name = []
        self.smiliar_domain_name = []
        self.related_domain_name = []
        self.email = []
        self.timeout = 25
        self.print_banner()
        self.results= ""
        return

    def run(self):
        domain_list = self.enumerate()
        for domain in domain_list:
            if "older.sublist3r" in domain:
                pass
            else:
                self.domain_name.append(domain)
        logger.info("{0} found {1} domains".format(self.engine_name, len(self.domain_name)))
        return self.domain_name,self.smiliar_domain_name,self.related_domain_name,self.email

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def req(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        }
        try:
            resp = req.get(url, headers=headers, timeout=self.timeout, proxies = self.proxy)
            return resp.content
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return None

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        self.results = self.req(url)
        return  self.get_hostnames()

    def get_hostnames(self):
        rawres = myparser.parser(self.results, self.domain)
        return rawres.hostnames()

if __name__ == "__main__":
    proxy = {"https":"https://127.0.0.1:9988","http":"http://127.0.0.1:9988"}
    proxy = {}
    x = PassiveDNS("meizu.com",proxy)
    print x.run()