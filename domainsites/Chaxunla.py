# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
#wydomain

import re
import time
import json
import logging

from lib.captcha import Captcha
from lib.common import is_domain

import requests
req = requests.Session()

class Chaxunla(object):
    """docstring for Chaxunla"""
    def __init__(self, domain, proxy=None):
        super(Chaxunla, self).__init__()
        self.domain = domain
        self.url = 'http://api.chaxun.la/toolsAPI/getDomain/'
        self.subset = []
        self.verify = ""
        self.engine_name= "Chaxunla"

    def run(self):

        try:
            timestemp = time.time()
            url = "{0}?0.{1}&callback=&k={2}&page=1&order=default&sort=desc&action=moreson&_={3}&verify={4}".format(
                self.url, timestemp, self.domain, timestemp, self.verify)
            result = json.loads(req.get(url).content)
            if result.get('status') == '1':
                for item in result.get('data'):
                    if is_domain(item.get('domain')):
                        self.subset.append(item.get('domain'))
            elif result.get('status') == 3:
                logging.info("chaxun.la api block you ip...")
                logging.info("input you verify_code in http://subdomain.chaxun.la/wuyun.org/")
                # print('get verify_code():', self.verify)
                # self.verify_code()
                # self.run()
            self.subset = list(set(self.subset))
            print "[-] {0} found {1} domains".format(self.engine_name, len(self.subset))
            return self.subset
        except Exception as e:
            logging.info(str(e))
            print "[-] {0} found {1} domains".format(self.engine_name, len(self.subset))
            return self.subset

    def download(self, url):
        try:
            r = req.get(url)
            with open("captcha.gif", "wb") as image:
                image.write(r.content)
            return True
        except Exception, e:
            return False

    def verify_code(self):
        timestemp = time.time()
        imgurl = 'http://api.chaxun.la/api/seccode/?0.{0}'.format(timestemp)
        if self.download(imgurl):
            captcha = Captcha()
            code_result = captcha.verification(filename='captcha.gif')
            self.verify = code_result.get('Result')


if __name__ == "__main__":
        x = Chaxunla("meizu.com",proxy="http://127.0.0.1:9999")
        print  x.run()
