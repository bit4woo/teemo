# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from lib.log import logger
from lib import myrequests
import config
import json
import urllib
req = myrequests
'''
this api need fee, pause to add to main function

其他相似付费接口
WHOXY	DOMAINTOOLS	WHOISXMLAPI	ROBOWHOIS	ZIPWHOIS

'''

class whoxy(object):
    def __init__(self, domain,proxy=None):
        self.domain = domain
        self.domain_name = []
        self.smiliar_domain_name = []
        self.related_domain_name = []
        self.email = []
        self.url= "http://api.whoxy.com/"
        self.engine_name = "Whoxy"
        try:
            self.api_key = config.Whoxy_API_KEY
        except:
            logger.warning("No Whoxy API Key Configured,Exit")
            exit(0)
        self.print_banner()
        self.proxy = proxy

        self.company_names = []
        self.company_emails = []
        self.company_phones = [] #该接口不支持
        '''
        whois查询其实可以有四种反查：
        公司名称
        联系人
        联系邮箱
        联系电话
        但whoxy并不是所有都支持https://www.whoxy.com/reverse-whois/demo.php
        '''

        self.blocked_names = []
        self.blocked_emails = []
        self.bChanged = False



    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def run(self):
        try:
            self.fetch()
            self.reverse_lookup()
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))
        finally:
            logger.info("{0} found {1} domains and {2} related_domains".format(self.engine_name, len(self.domain_name),len(self.related_domain_name)))
            return self.domain_name,self.smiliar_domain_name,self.related_domain_name,self.email

    def fetch(self):
        try:
            url = '{0}?key={1}&whois={2}'.format(self.url, self.api_key, self.domain)
            r = req.get(url,proxies = self.proxy)
            content = json.loads(r.text)
            if (content["status"] != 1):
                logger.error("[!] WHOIS lookup failed, your whoxy API key is probably invalid or credits have been exhausted")
            else:
                self.company_names.append(content["registrant_contact"]["company_name"].lower())
                self.company_emails.append(content["registrant_contact"]["email_address"].lower())
                self.company_phones.append(content["registrant_contact"]["phone_number"])

                self.company_names.append(content["administrative_contact"]["company_name"].lower())
                self.company_emails.append(content["administrative_contact"]["email_address"].lower())
                self.company_phones.append(content["administrative_contact"]["phone_number"])

                self.company_names.append(content["technical_contact"]["company_name"].lower())
                self.company_emails.append(content["technical_contact"]["email_address"].lower())
                self.company_phones.append(content["technical_contact"]["phone_number"])

                self.company_names.append(content["billing_contact"]["company_name"].lower())
                self.company_emails.append(content["billing_contact"]["email_address"].lower())
                self.company_phones.append(content["billing_contact"]["phone_number"])

            self.company_names = list(set(self.company_names))
            self.company_emails = list(set(self.company_emails))
            self.company_phones = list(set(self.company_phones))

        except Exception,e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))


    def reverse_lookup(self):
        logger.info("Performing Reverse WHOIS lookup in Whoxy")
        for company_name in self.company_names:
            pages = 10
            cur_page = 1

            while (cur_page - 1 < pages):
                url = "{0}?key={1}&reverse=whois&company={2}&mode=mini&page={3}".format(self.url,self.api_key, urllib.quote(company_name), cur_page)
                r = req.get(url,proxies=self.proxy)
                content = json.loads(r.text)
                # print content
                if content["status"] == 1:
                    pages = content["total_pages"]
                    for result in content["search_result"]:
                        try:
                            if result["domain_name"].lower().endswith(".{0}".format(self.domain)):
                                self.domain_name.append(result["domain_name"])
                            else:
                                self.related_domain_name.append(result["domain_name"])

                            if not (result["company_name"].lower() in self.company_names):
                                self.company_names.append(result["company_name"].lower())

                            if config.Reverse_Email_Confirm: #手动判断
                                if result["email_address"].lower() not in self.company_emails and result["email_address"].lower() not in self.blocked_emails:
                                    bAdd = raw_input("[*] Do you want to add '%s' as a company email? (Y/n):" % result[
                                        "email_address"]).upper()
                                    if bAdd == "" or bAdd == "Y":
                                        bAdd = "Y"
                                    else:
                                        bAdd = "N"
                            else:#自动判断
                                if self.domain.lower().split(".")[0] in  result["email_address"].lower():
                                    bAdd = "Y"
                                else:
                                    bAdd = "N"

                            if bAdd == "Y":
                                self.company_emails.append(result["email_address"].lower())
                            else:
                                self.blocked_emails.append(result["email_address"].lower())
                        except:
                            continue
                cur_page += 1

        # Emails now

        for company_email in self.company_emails:
            pages = 10
            cur_page = 1

            while (cur_page - 1 < pages):
                url = "{0}?key={1}&reverse=whois&email={2}&mode=mini&page={3}".format(self.url,self.api_key, urllib.quote(company_email), cur_page)

                r = req.get(url,proxies=self.proxy)
                content = json.loads(r.text)
                # print content
                if content["status"] == 1:
                    pages = content["total_pages"]
                    for result in content["search_result"]:
                        try:
                            if result["domain_name"].endswith(".{0}".format(self.domain)):
                                self.domain_name.append(result["domain_name"])
                            else:
                                self.related_domain_name.append(result["domain_name"])

                            if not (result["company_name"].lower() in self.company_names):
                                self.company_names.append(result["company_name"])

                            if not (result["email_address"].lower() in self.company_emails):
                                self.company_emails.append(result["email_address"])

                        except:
                            continue
                cur_page += 1

if __name__ == "__main__":
        proxy = {"http":"http://127.0.0.1:9988"}
        proxy = {}
        x = whoxy("pingan.com",proxy=proxy)
        print  x.run()
        print x.company_emails
        print x.company_names
        print x.company_phones