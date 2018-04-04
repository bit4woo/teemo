# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
'''
related domains

'''
from lib.log import logger
from lib.myparser import parser
from lib import myrequests
import re
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
        self.related_domain_name = []
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
                self.get_related_domains()
                self.related_domain_name = list(set(self.related_domain_name))
            for domain in self.subdomains:
                self.domain_name.append(domain)
        except Exception,e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
        finally:
            logger.info("{0} found {1} domains and {2} related_domains".format(self.engine_name, len(self.domain_name),len(self.related_domain_name)))
            return self.domain_name,self.smiliar_domain_name,self.related_domain_name,self.email

    def get_hostnames(self):
        rawres = parser(self.resp, self.domain)
        return rawres.hostnames()
    def get_email(self):
        rawres = parser(self.resp, self.domain)
        return rawres.emails()
    def get_related_domains(self):
        result = []
        reg_urls = re.compile('<A href="(.*?)"')#<A href="?id=312991737">
        urls = reg_urls.findall(self.resp)

        reg_domains = re.compile('DNS:(.*?)<BR>') #DNS:*.jdpay.com<BR>
        for item in urls:
            url = "https://crt.sh/{0}".format(item)
            resp = req.get(url, proxies=self.proxy).content
            tmp = reg_domains.findall(resp)
            result.extend(tmp)

        for domain in result:
            domain = domain.lower()
            if domain.startswith("*."):
                domain = domain.replace("*.","")
            if domain.endswith(".{0}".format(self.domain)):
                self.domain_name.append(domain)
            else:
                self.related_domain_name.append(domain)
        self.related_domain_name = list(set(self.related_domain_name))

if __name__ == "__main__":
    proxy = {"http":"http://127.0.0.1:9988"}
    #proxy = {}
    x= CrtSearch("jd.hk",proxy)
    print x.run()
