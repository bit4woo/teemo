# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
import re
import requests

class DNSdumpster():
    def __init__(self, domain, proxy=None):
        self.subdomains = []
        self.base_url = 'https://dnsdumpster.com/'
        self.engine_name = "DNSdumpster"
        self.session= requests.session()
        self.q = []
        self.domain =domain
        self.timeout = 10
        return

    def run(self):
        domain_list = self.enumerate()
        for domain in domain_list:
            self.q.append(domain)
        print "[-] {0} found {1} domains".format(self.engine_name, len(self.q))
        return self.q


    def req(self, req_method, url, params=None):
        params = params or {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://dnsdumpster.com'
        }

        try:
            if req_method == 'GET':
                resp = self.session.get(url, headers=headers, timeout=self.timeout)
            else:
                resp = self.session.post(url, data=params, headers=headers, timeout=self.timeout)
        except Exception as e:
            print e
            return None
        if hasattr(resp, "text"):
            return resp.text
        else:
            return resp.content

    def get_csrftoken(self, resp):
        csrf_regex = re.compile("<input type='hidden' name='csrfmiddlewaretoken' value='(.*?)' />", re.S)
        token = csrf_regex.findall(resp)[0]
        return token.strip()

    def enumerate(self):
        resp = self.req('GET', self.base_url)
        token = self.get_csrftoken(resp)
        params = {'csrfmiddlewaretoken': token, 'targetip': self.domain}
        post_resp = self.req('POST', self.base_url, params)
        self.extract_domains(post_resp)
        return self.subdomains

    def extract_domains(self, resp):
        tbl_regex = re.compile('<a name="hostanchor"><\/a>Host Records.*?<table.*?>(.*?)</table>', re.S)
        link_regex = re.compile('<td class="col-md-4">(.*?)<br>', re.S)
        links = []
        try:
            results_tbl = tbl_regex.findall(resp)[0]
        except IndexError:
            results_tbl = ''
        links_list = link_regex.findall(results_tbl)
        links = list(set(links_list))
        for link in links:
            subdomain = link.strip()
            if not subdomain.endswith(self.domain):
                continue
            if subdomain and subdomain not in self.subdomains and subdomain != self.domain:
                self.subdomains.append(subdomain.strip())
        return links

if __name__ == "__main__":
    x = DNSdumpster("meizu.com")
    print x.run()