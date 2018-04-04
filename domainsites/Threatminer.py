# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib.log import logger
from lib.myparser import parser
from lib import myrequests
req = myrequests


class Threatminer():
    def __init__(self, domain, proxy=None):
        #self.domain = urlparse.urlparse(domain).netloc
        self.proxy = proxy
        self.domain = domain
        self.subdomains = []
        self.engine_name = "Threatminer"
        self.timeout = 25
        self.print_banner()
        self.website = "https://www.threatminer.org"
        self.domain_name = []
        self.smiliar_domain_name = []
        self.related_domain_name = []
        self.email = []
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def run(self):
        try:
            url = "{0}/getData.php?e=subdomains_container&q={1}&t=0&rt=10&p=1".format(self.website, self.domain)
            # content = curl_get_content(url).get('resp')
            content = req.get(url,proxies = self.proxy).content

            rawres = parser(content, self.domain)
            self.domain_name = rawres.hostnames()
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))

        logger.info("{0} found {1} domains".format(self.engine_name, len(self.domain_name)))
        return self.domain_name,self.smiliar_domain_name,self.related_domain_name,self.email

if __name__ == "__main__":
    proxy = {"https":"https://127.0.0.1:9988","http":"http://127.0.0.1:9988"}
    proxy = {}
    x = Threatminer("meizu.com",proxy)
    print x.run()