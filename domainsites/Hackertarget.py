# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib.myparser import parser
from lib.log import logger
from lib import myrequests
req = myrequests

class Hackertarget(object):
    def __init__(self, domain,proxy=None):
        self.domain = domain
        self.domain_name = []
        self.smiliar_domain_name = []
        self.related_domain_name = []
        self.email = []
        self.url= "https://api.hackertarget.com/"
        self.engine_name = "HackerTarget"
        self.print_banner()
        self.proxy = proxy

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def run(self):
        try:
            self.fetch()
            self.domain_name = list(set(self.domain_name))
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))
        finally:
            logger.info("{0} found {1} domains".format(self.engine_name, len(self.domain_name)))
            return self.domain_name,self.smiliar_domain_name,self.related_domain_name,self.email

    def fetch(self):
        url = '{0}hostsearch/?q={1}'.format(self.url,self.domain)
        try:
            r = req.get(url,proxies = self.proxy).content
            rawres = parser(r, self.domain)
            result = rawres.hostnames()
            for sub in result:
                self.domain_name.append(sub)
        except Exception,e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))


if __name__ == "__main__":
        proxy = {"http":"http://127.0.0.1:9988"}
        proxy = {}
        x = Hackertarget("meizu.com",proxy=proxy)
        print  x.run()