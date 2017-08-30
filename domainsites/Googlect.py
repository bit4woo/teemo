# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
#wydomain

from lib.common import *
from lib.log import logger
import time
import urllib
from random import Random,uniform #googlect

class Googlect():
    #https://www.google.com/transparencyreport/jsonp/ct/search?domain=apple.com&incl_exp=true&incl_sub=true&token=CAo%3D&c=_callbacks_._4ixpyevsd
    def __init__(self, domain, proxy=None):
        self.verify = ""
        #self.domain = urlparse.urlparse(domain).netloc
        self.domain = domain
        self.token = ""
        self.dns_names = []
        self.subjects = []
        self.hashs = []
        self.num_result = 0
        self.website = 'https://www.google.com/transparencyreport/jsonp/ct'
        self.subdomains = []
        self.engine_name = "GoogleCT"
        self.timeout = 25
        self.print_banner()
        self.proxy = proxy
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
        self.hashs = list(set(self.hashs)) # unique sort hash
        self.parser_dnsname()
        self.dns_names = list(set(self.dns_names))
        #self.subjects = list(set(self.subjects))
        logger.info("{0} found {1} domains".format(self.engine_name, len(self.dns_names)))
        return self.dns_names
    def req(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        }
        try:
            resp = requests.get(url, headers=headers, timeout=self.timeout,proxies = self.proxy)
            if hasattr(resp, "text"):
                return resp.text
            else:
                return resp.content
        except Exception as e:
            print e
            return 0
    def parser_subject(self):
        #try:
        callback = self.random_str()
        url = '{0}/search?domain={1}&incl_exp=true&incl_sub=true&token={2}&c={3}'.format(
                self.website, self.domain, urllib.quote(self.token), callback)
        content = self.req(url)
        result = json.loads(content[27:-3])
        self.token = result.get('nextPageToken')
        for subject in result.get('results'):
            if subject.get('subject'):
                self.dns_names.append(subject.get('subject'))
            if subject.get('hash'):
                self.hashs.append(subject.get('hash'))
        #except Exception as e:
            #print e.message
            #pass

        if self.token:
            self.parser_subject()

    def parser_dnsname(self):
        for hashstr in self.hashs:
            try:
                callback = self.random_str()
                url = '{0}/cert?hash={1}&c={2}'.format(
                        self.website, urllib.quote(hashstr), callback)
                content = http_request_get(url, proxies=self.proxy).content
                result = json.loads(content[27:-3])
                if result.get('result').get('subject'):
                    self.subjects.append(result.get('result').get('subject'))
                if result.get('result').get('dnsNames'):
                    self.dns_names.extend(result.get('result').get('dnsNames'))
            except Exception as e:
                pass
            self.random_sleep()

if __name__ == "__main__":
    proxy = {"https":"https://127.0.0.1:9988"}
    x = Googlect("welab.co",proxy)
    #print x.parser_dnsname()
    print x.run()