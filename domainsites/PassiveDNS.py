# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

#this can search email address ,but not returned
from lib import myparser
from lib.log import logger
import requests

class PassiveDNS():
    def __init__(self, domain, proxy=None):
        self.base_url = 'http://ptrarchive.com/tools/search.htm?label={domain}'
        self.domain = domain
        self.subdomains = []
        self.session = requests.Session()
        self.engine_name = "PassiveDNS"
        self.q = []
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
                self.q.append(domain)
        logger.info("{0} found {1} domains".format(self.engine_name, len(self.q)))
        return self.q

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
            resp = requests.get(url, headers=headers, timeout=self.timeout)
            return resp.content
        except Exception as e:
            logger.error(e)
            return None

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        self.results = self.req(url)
        return  self.get_hostnames()

    def get_hostnames(self):
        rawres = myparser.parser(self.results, self.domain)
        return rawres.hostnames()

if __name__ == "__main__":
    x = PassiveDNS("meizu.com","https://127.0.0.1:9999")
    print x.run()