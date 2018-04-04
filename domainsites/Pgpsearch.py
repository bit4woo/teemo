# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import httplib
from lib import myparser
from lib.log import logger
from lib import myrequests
req = myrequests
# to do :return emails

class Pgpsearch:

    def __init__(self, domain, proxy = None):
        self.domain = domain
        self.proxy = proxy
        self.results = ""
        self.url = "http://pgp.mit.edu/pks/lookup?search={domain}&op=index".format(domain =self.domain)
        #self.server = "pgp.rediris.es:11371" Not  working at the moment
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.engine_name = "PGP"
        self.domain_name = []
        self.smiliar_domain_name = []
        self.related_domain_name = []
        self.email = []
        self.timeout = 25
        self.print_banner()

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def process(self):
        try:
            resp = req.get(url=self.url,proxies = self.proxy,timeout = self.timeout)
            self.results = resp.content
        except Exception,e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))

    def get_emails(self):
        rawres = myparser.parser(self.results, self.domain)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.results, self.domain)
        return rawres.hostnames()
    def run(self):
        self.process()
        self.domain_name = self.get_hostnames() # how to receive emails.
        self.email = self.get_emails()
        logger.info("{0} found {1} domains and {2} emails".format(self.engine_name, len(self.domain_name), len(self.email)))
        return self.domain_name,self.smiliar_domain_name,self.related_domain_name,self.email

if __name__ == "__main__":
    proxy = {"https":"https://127.0.0.1:9988","http":"http://127.0.0.1:9988"}
    proxy = {}
    x= Pgpsearch("meizu.com",proxy)
    print x.run()