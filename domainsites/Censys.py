# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib.myparser import parser
from lib.log import logger
from lib import myrequests
import censys.certificates
import config
import tldextract #https://github.com/john-kurkowski/tldextract 获取一个域名的主域名 比如 pingan.com pingan.com.cn
req = myrequests


'''
related domains : get by cert SANs
提取相关域名的核心方法之一
'''

class Censys(object):
    def __init__(self, domain,proxy=None):
        self.domain = domain
        self.domain_name = []
        self.smiliar_domain_name = []
        self.related_domain_name = []
        self.email = []
        self.url= "https://censys.io/api/v1"
        self.engine_name = "Censys"
        try:
            self.api_id = config.Censys_API_UID
            self.api_secret = config.Censys_API_SECRET
        except:
            logger.warning("No Censys API Config,Exit")
            exit(0)
        self.print_banner()
        self.proxy = proxy

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def run(self):
        try:
            self.search()
            self.domain_name = list(set(self.domain_name))
            self.related_domain_name = list(set(self.related_domain_name))
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))
        finally:
            logger.info("{0} found {1} domains and {2} related_domains".format(self.engine_name, len(self.domain_name), len(self.related_domain_name)))
            return self.domain_name,self.smiliar_domain_name,self.related_domain_name,self.email

    def search(self):
        temp_domains = []
        try:
            main_of_domain = tldextract.extract(self.domain).domain
            c = censys.certificates.CensysCertificates(api_id=self.api_id, api_secret=self.api_secret)

            # iterate over certificates that match a search
            fields = ["parsed.subject_dn", "parsed.fingerprint_sha256"] #parsed.issuer_dn
            for cert in c.search("{0}".format(self.domain), fields=fields):
                #print cert["parsed.subject_dn"]
                cn_domain= cert["parsed.subject_dn"].split(",")[-1].split("=")[-1]#cn一定是在最后吗
                main_of_cn_domain =tldextract.extract(cn_domain).domain

                if main_of_domain in main_of_cn_domain:
                    detail = c.view(cert["parsed.fingerprint_sha256"]) #print c.view("a762bf68f167f6fbdf2ab00fdefeb8b96f91335ad6b483b482dfd42c179be076")
                    #print detail
                    #print detail["parsed"]["names"]
                    temp_domains.extend(detail["parsed"]["names"])
                    temp_domains = list(set(temp_domains))
        except Exception,e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))
        #
        for domain in temp_domains:
            domain = domain.lower()
            if domain.startswith("*."):
                domain = domain.replace("*.","")
            if domain == self.domain:
                self.domain_name.append(domain)
            elif domain.endswith(".{0}".format(self.domain)):
                self.domain_name.append(domain)
            else:
                self.related_domain_name.append(domain)

if __name__ == "__main__":
        proxy = {"http":"http://127.0.0.1:9988","https":"https://127.0.0.1:9988"}
        #proxy = {}
        x = Censys("jd.hk",proxy=proxy)
        print  x.run()



