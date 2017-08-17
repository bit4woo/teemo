# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import requests
from lib.log import logger
from lib.myparser import parser
from lib.common import http_request_get

class CrtSearch():
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
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def run(self):
        url = self.base_url.format(domain=self.domain)
        #print url
        try:
            self.resp = http_request_get(url).content
            if self.resp:
                self.subdomains = self.get_hostnames()
            for domain in self.subdomains:
                self.q.append(domain)
        except Exception,e:
            logger.error(e)
        finally:
            logger.info("{0} found {1} domains".format(self.engine_name, len(self.q)))
            return self.q

    def get_hostnames(self):
        rawres = parser(self.resp, self.domain)
        return rawres.hostnames()

if __name__ == "__main__":
    x= CrtSearch("meizu.com")
    print x.run()