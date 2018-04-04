# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib.common import *
from lib.log import logger
from lib import myrequests
req = myrequests

'''
website offline
'''

class Ilink():
    def __init__(self, domain, proxy=None):
        self.url = 'http://i.links.cn/subdomain/'
        self.proxy = proxy
        #self.domain = urlparse.urlparse(domain).netloc
        self.domain = domain
        self.subdomains = []
        self.engine_name = "Ilinks"
        self.domain_name = []
        self.smiliar_domain_name = []
        self.related_domain_name = []
        self.email = []
        self.timeout = 25
        self.print_banner()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def run(self):
        try:
            payload = {
                'b2': 1,
                'b3': 1,
                'b4': 1,
                'domain': self.domain
            }
            r = req.post(self.url,data=payload,proxies=self.proxy).content
            subs = re.compile(r'(?<=value\=\"http://).*?(?=\"><input)')
            for item in subs.findall(r):
                if is_domain(item):
                    self.domain_name.append(item)

            self.domain_name = list(set(self.domain_name))
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
        finally:
            logger.info("{0} found {1} domains".format(self.engine_name, len(self.domain_name)))
            return self.domain_name,self.smiliar_domain_name,self.related_domain_name,self.email

if __name__ == "__main__":
    proxy = {"https":"https://127.0.0.1:9988","http":"http://127.0.0.1:9988"}
    #proxy = {}
    x = Ilink("meizu.com",proxy)
    print x.run()