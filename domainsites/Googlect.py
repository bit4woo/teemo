# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
'''
#根据证书返回结构，会返回带*号的域名，可用于查找属于同机构的多个域名，和相似域名。
# 主要作用是查找同一机构的相关域名
# web页面 https://transparencyreport.google.com/https/certificates
# 搜索页面 https://transparencyreport.google.com/https/certificates?cert_search_auth=&cert_search_cert=&cert_search=include_expired:true;include_subdomains:true;domain:jd.hk&lu=cert_search
# 详情页面 https://transparencyreport.google.com/https/certificates/AQNUDDPJ1PH9UuZp1gqt0zWLLz7nn1WgP/UzA5XRTZs=

# 搜索接口: https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch?domain=jd.hk&include_expired=true&include_subdomains=true
# 详情接口：https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certbyhash?hash=AQNUDDPJ1PH9UuZp1gqt0zWLLz7nn1WgP/UzA5XRTZs=
'''

from lib.log import logger
import time
from lib.myparser import parser
from random import Random,uniform #googlect
import ast
import tldextract
from lib import myrequests
req = myrequests
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    pass

class Googlect():
    def __init__(self, domain, proxy=None):
        self.verify = ""
        #self.domain = urlparse.urlparse(domain).netloc
        self.domain = domain
        self.token = ""
        self.num_result = 0
        self.search_api = "https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch?domain={0}&include_expired=true&include_subdomains=true"
        self.detail_url = "https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certbyhash?hash={0}"
        self.hash_codes = []
        self.engine_name = "GoogleCert"
        self.timeout = 10
        self.print_banner()
        self.proxy = proxy
        self.domain_name = []
        self.smiliar_domain_name = []
        self.related_domain_name = []
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
        self.get_related_domains()
        self.domain_name = list(set(self.domain_name))
        self.related_domain_name = list(set(self.related_domain_name))
        logger.info("{0} found {1} domains and {2} related_domains ".format(self.engine_name, len(self.domain_name), len(self.related_domain_name)))
        return self.domain_name,self.smiliar_domain_name,self.related_domain_name,self.email
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
            url = self.search_api.format(self.domain)
            if self.req(url):
                formated_string = (self.result[6:-1]).replace("\n","").replace("[","").replace("]","")
                self.token = formated_string.split(",")[-4]
                #print result
                #total_page = (self.result[6:-1]).replace("\n","").replace("[","").replace("]","").split(",")[-1]
                #current_page = (self.result[6:-1]).replace("\n", "").replace("[", "").replace("]", "").split(",")[-2]
                #it seems that no need to switch pages, the main purpose of this API is to get the related domains. it's enough using items in one page

                rawres = parser(self.result, self.domain)
                domains = rawres.hostnames()
                if domains!= None:
                    self.domain_name.extend(domains)

                for item in formated_string.split(","): #
                    if len(item) >=40 and " " not in item:#sSWg6vIw46sI1eNhDlilAaanXC9htQlVuMuHJWqyNr8=
                        item = item.strip("\"")
                        #item = unicode(item).decode()
                        item = item.replace("\\u003d","=")
                        self.hash_codes.append(item)
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return

    def get_related_domains(self):
        if self.hash_codes > 0:
            main_of_domain = tldextract.extract(self.domain).domain
            for hash in self.hash_codes:
                try:
                    url = self.detail_url.format(hash)
                    resp = req.get(url, timeout=self.timeout, proxies=self.proxy, verify=False)
                    if resp:
                        formated_string = (self.result[6:-1]).replace("\n", "")
                        tmplist = ast.literal_eval(formated_string) #把list格式的string转换成list

                        main_of_cn_domain = tmplist[0][1][1].split(",")[-1]

                        if "CN\u003d" in main_of_cn_domain:#有可能响应的内容为空，判断一下
                            main_of_cn_domain = main_of_cn_domain.replace("CN\u003d","")
                            main_of_cn_domain = tldextract.extract(main_of_cn_domain).domain
                            if main_of_domain in main_of_cn_domain: #判断cn中的域名是否和要查询的域名相似
                                self.related_domain_name.extend(tmplist[0][1][-1])
                        else:
                            continue
                except Exception,e:
                    logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))
                    return

        for domain in self.related_domain_name:
            domain = domain.lower()
            if domain.startswith("*."):
                domain = domain.replace("*.", "")

            if domain == self.domain:
                self.domain_name.append(domain)
            elif domain.endswith(".{0}".format(self.domain)):
                self.domain_name.append(domain)
            else:
                self.related_domain_name.append(domain)
        self.related_domain_name = list(set(self.related_domain_name))


if __name__ == "__main__":
    proxy = {"https":"https://127.0.0.1:9988"}
    proxy = {}
    x = Googlect("meizu.com",proxy)
    print x.run()