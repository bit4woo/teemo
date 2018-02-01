# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
#根据证书返回结构，会返回带*号的域名，可用于查找属于同机构的多个域名，和相似域名。

from lib.log import logger
import time
from lib.myparser import parser
from random import Random,uniform #googlect
import ast
from lib import myrequests
req = myrequests
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    pass

class Googlect():
    #https://www.google.com/transparencyreport/jsonp/ct/search?domain=apple.com&incl_exp=true&incl_sub=true&token=CAo%3D&c=_callbacks_._4ixpyevsd
    #https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch?include_expired=true&include_subdomains=true&domain=jd.com
    def __init__(self, domain, proxy=None):
        self.verify = ""
        #self.domain = urlparse.urlparse(domain).netloc
        self.domain = domain
        self.token = ""
        self.dns_names = []
        self.subjects = []
        self.hashs = []
        self.num_result = 0
        self.website = 'https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct'
        self.subdomains = []
        self.engine_name = "GoogleCT"
        self.timeout = 10
        self.print_banner()
        self.proxy = proxy
        self.domain_name = []
        self.smiliar_domain_name = []
        self.email = []
        self.result = ""
        return

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def random_sleep(self):
        time.sleep(uniform(0,2))

    def random_str(self, randomlength=8):
        rstr = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(randomlength):
            rstr += chars[random.randint(0, length)]
        return rstr.lower()

    def run(self):
        self.parser_subject()
        self.dns_names = list(set(self.dns_names))
        for item in self.dns_names:
            if self.domain in item:
                self.domain_name.append(item)
            else:
                self.smiliar_domain_name.append(item)
        #self.subjects = list(set(self.subjects))
        logger.info("{0} found {1} domains".format(self.engine_name, len(self.dns_names)))
        return self.domain_name,self.smiliar_domain_name,self.email
    def req(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        }
        try:
            resp = req.get(url, headers=headers, timeout=self.timeout,proxies = self.proxy,verify=False)
            if resp.status_code == 200:
                if hasattr(resp, "text"):
                    self.result = resp.text
                else:
                    self.result = resp.content
                return True
            else:
                logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], resp.reason))
                return False
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return False
    def parser_subject(self):
        try:
            #certsearch?include_expired=true&include_subdomains=true&domain=jd.com
            url = '{0}/certsearch?domain={1}&include_expired=true&include_subdomains=true'.format(
                self.website, self.domain)
            if self.req(url):
                result = (self.result[6:-1]).replace("\n","").replace("[","").replace("]","").split(",")[-4]
                total_page = (self.result[6:-1]).replace("\n","").replace("[","").replace("]","").split(",")[-1]
                current_page = (self.result[6:-1]).replace("\n", "").replace("[", "").replace("]", "").split(",")[-2]
                self.token = ast.literal_eval(result)
                rawres = parser(self.result, self.domain)
                domains = rawres.hostnames()
                if domains!= None:
                    self.dns_names.extend(domains)
                '''
                while current_page < total_page:#重复请求，页面未变，该如何修改页面呢？
                    url = "https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch/page?p={0}".format(self.token)
                    if self.req(url):
                        print "xxxxx"
                        current_page = \
                        (self.result[6:-1]).replace("\n", "").replace("[", "").replace("]", "").split(",")[-2]
                        print current_page
                        rawres = parser(self.result, self.domain)
                        domains = rawres.hostnames()
                        self.dns_names.extend(domains)
                    else:
                        break
                '''
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return

if __name__ == "__main__":
    proxy = {"https":"https://127.0.0.1:9988"}
    proxy = {}
    x = Googlect("meizu.com",proxy)
    #print x.parser_dnsname()
    print x.run()