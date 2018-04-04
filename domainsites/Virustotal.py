# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import re
from lib.log import logger
from lib import myrequests
req = myrequests

class Virustotal():
    def __init__(self, domain, proxy=None):
        self.base_url = 'https://www.virustotal.com/en/domain/{domain}/information/'
        self.proxy = proxy
        self.domain = domain
        self.subdomains = []
        self.engine_name = "Virustotal"
        self.domain_name = []
        self.smiliar_domain_name = []
        self.related_domain_name = []
        self.email = []
        self.timeout = 10
        self.print_banner()
        return

    def run(self):
        domain_list = self.enumerate()
        for domain in domain_list:
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
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))
            resp = None

        return self.get_response(resp)

    def get_response(self,response):
        if response is None:
            return None
        if hasattr(response, "text"):
            return response.text
        else:
            return response.content

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.req(url)
        self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        link_regx = re.compile('<div class="enum.*?">.*?<a target="_blank" href=".*?">(.*?)</a>',re.S)
        try:
            links = link_regx.findall(resp)
            for link in links:
                subdomain = link.strip()
                if not subdomain.endswith(self.domain):
                    continue
                if subdomain not in self.subdomains and subdomain != self.domain:
                    #if verbose:
                        #print "%s%s: %s%s"%(R, self.engine_name, W, subdomain)
                    self.subdomains.append(subdomain.strip())
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))


if __name__ == "__main__":
    proxy = {"https":"https://127.0.0.1:9988","http":"http://127.0.0.1:9988"}
    #proxy = {}
    x = Virustotal("meizu.com",proxy)
    print x.run()