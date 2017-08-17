# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib.common import http_request_get
from lib.myparser import parser
from lib.log import logger

class Alexa(object):
    """docstring for Alexa"""
    def __init__(self, domain,proxy=None):
        super(Alexa, self).__init__()
        self.domain = domain
        self.subset = []
        self.url= "http://alexa.chinaz.com/"
        self.engine_name = "Alexa"
        self.print_banner()

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def run(self):
        try:
            self.fetch_chinaz()
            self.subset = list(set(self.subset))
        except Exception as e:
            logger.info(str(e))
        finally:
            logger.info("{0} found {1} domains".format(self.engine_name, len(self.subset)))
            return self.subset


    def fetch_chinaz(self):
        """get subdomains from alexa.chinaz.com"""

        url = '{0}?domain={1}'.format(self.url,self.domain)
        r = http_request_get(url).content
        rawres = parser(r, self.domain)
        result = rawres.hostnames()
        for sub in result:
            self.subset.append(sub)

if __name__ == "__main__":
        x = Alexa("meizu.com",proxy="http://127.0.0.1:9999")
        print  x.run()