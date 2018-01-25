# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib.log import logger
from lib.myparser import parser
from lib import myrequests
req = myrequests

class CrtSearch():
    def __init__(self, domain, proxy=None):
        self.proxy = proxy
        self.base_url = 'https://crt.sh/?q=%25.{domain}'
        #self.domain = urlparse.urlparse(domain).netloc
        self.resp = ""
        self.domain = domain
        self.subdomains = []
        self.engine_name = "crt.sh"
        self.domain_name = []
        self.smiliar_domain_name = []
        self.email = []
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
            self.resp = req.get(url,proxies=self.proxy).content
            if self.resp:
                self.subdomains = self.get_hostnames()
                self.email = self.get_email()
            for domain in self.subdomains:
                self.domain_name.append(domain)
        except Exception,e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
        finally:
            logger.info("{0} found {1} domains".format(self.engine_name, len(self.domain_name)))
            return self.domain_name,self.smiliar_domain_name,self.email

    def get_hostnames(self):
        rawres = parser(self.resp, self.domain)
        return rawres.hostnames()
    def get_email(self):
        rawres = parser(self.resp, self.domain)
        return rawres.emails()

if __name__ == "__main__":
    proxy = {"http":"http://127.0.0.1:9988"}
    #proxy = {}
    x= CrtSearch("jd.com",proxy)
    print x.run()
