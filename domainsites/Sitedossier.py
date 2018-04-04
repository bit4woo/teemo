# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib.captcha import *
from lib.log import logger
import re
from lib import myrequests
req = myrequests

class Sitedossier():
    def __init__(self, domain, proxy=None):
        #self.domain = urlparse.urlparse(domain).netloc
        self.proxy = proxy
        self.domain = domain
        self.url = 'http://www.sitedossier.com/parentdomain/{0}'.format(self.domain)
        self.subdomains = []
        self.engine_name = "Sitedossier"
        self.domain_name = []
        self.smiliar_domain_name = []
        self.related_domain_name = []
        self.email = []
        self.timeout = 25
        self.print_banner()
        self.captcha = Captcha()
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def run(self):
        try:
            r = self.get_content(self.url)
            self.parser(r)
            self.domain_name = list(set(self.domain_name))
        except Exception, e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))

        logger.info("{0} found {1} domains".format(self.engine_name, len(self.domain_name)))
        return self.domain_name,self.smiliar_domain_name,self.related_domain_name,self.email

    def get_content(self, url):
        #logger.info('request: {0}'.format(url))
        r = req.get(url,proxies = self.proxy).text
        if self.human_act(r) is True:
            return r
        else:
            self.get_content(url)

    def parser(self, response):
        npage = re.search('<a href="/parentdomain/(.*?)"><b>Show', response)
        if npage:
            for sub in self.get_subdomain(response):
                self.domain_name.append(sub)
            nurl = 'http://www.sitedossier.com/parentdomain/{0}'.format(npage.group(1))
            response = self.get_content(nurl)
            self.parser(response)
        else:
            for sub in self.get_subdomain(response):
                self.domain_name.append(sub)

    def get_subdomain(self, response):
        domain = re.compile(r'(?<=<a href\=\"/site/).*?(?=\">)')
        for sub in domain.findall(response):
            yield sub

    def human_act(self, response):
        if 'auditimage' in response or 'blacklisted' in response:
            imgurl = self.get_audit_img(response)
            if imgurl is not None:
                ret = self.captcha.verification(imgurl)
                if ret.has_key('Result'):
                    self.audit(ret['Result'])
                    return True
                else:
                    raise Exception("captcha_verification_is_empty")
            else:
                raise Exception("audit_img_is_empty")
        else:
            return True

    def audit(self, code):
        payload = {'w':code}
        url = 'http://www.sitedossier.com/audit'
        r = req.post(url, data=payload, proxies = self.proxy)

    def get_audit_img(self, response):
        auditimg = re.compile(r'(?<=<img src\=\"/auditimage/).*?(?=\?" alt="Please)')
        imgurl = auditimg.findall(response)[0:]
        if len(imgurl) >= 1:
            imgurl = 'http://www.sitedossier.com/auditimage/{0}'.format(imgurl[0])
            return imgurl
        else:
            return None

    def __str__(self):
        handler = lambda e: str(e)
        return json.dumps(self, indent=2, default=handler)

if __name__ == "__main__":
    proxy = {"https":"https://127.0.0.1:9988","http":"http://127.0.0.1:9988"}
    #proxy = {}
    x = Sitedossier("meizu.com",proxy)
    print x.run()