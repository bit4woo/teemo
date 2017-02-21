__author__ = 'bit4'
import multiprocessing
import threading
import urlparse
import dns
import requests
import re


class DNSdumpster():
    def __init__(self, domain, proxy=None):
        self.base_url = 'https://dnsdumpster.com/'
        self.domain = urlparse.urlparse(domain).netloc
        self.subdomains = []
        self.live_subdomains = []
        self.session = requests.Session()
        self.engine_name = "DNSdumpster"
        self.q = []
        self.timeout = 25
        self.print_banner()
        return

    def run(self):
        domain_list = self.enumerate()
        for domain in domain_list:
            self.q.append(domain)
        print "[-] {0} found {1} domains".format(self.engine_name, len(self.q))
        return self.q

    def print_banner(self):
        print "[-] Searching now in %s" %(self.engine_name)
        return

    def check_host(self,host):
        is_valid = False
        Resolver = dns.resolver.Resolver()
        Resolver.nameservers = ['8.8.8.8', '8.8.4.4']
        try:
            ip = Resolver.query(host, 'A')[0].to_text()
            if ip:
                #if verbose:
                   # print "%s%s: %s%s"%(R, self.engine_name, W, host)
                is_valid = True
                self.live_subdomains.append(host)
        except:
            pass
        return is_valid

    def req(self, req_method, url, params=None):
        params = params or {}
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
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
            resp = None
        return self.get_response(resp)

    def get_response(self,response):
        if response is None:
            return None
        if hasattr(response, "text"):
            return response.text
        else:
            return response.content

    def get_csrftoken(self, resp):
        csrf_regex = re.compile("<input type='hidden' name='csrfmiddlewaretoken' value='(.*?)' />",re.S)
        token = csrf_regex.findall(resp)[0]
        #print token
        return token.strip()


    def enumerate(self):
        resp = self.req('GET', self.base_url)
        #print resp
        token = self.get_csrftoken(resp)
        params = {'csrfmiddlewaretoken':token, 'targetip':self.domain}
        post_resp = self.req('POST', self.base_url, params)
        if "Too many requests from your IP address, temporary limit enforced. Try again tomorrow." in post_resp:
            print "[!] Error: DNSdumpster has blocked our request"
        self.extract_domains(post_resp)
        for subdomain in self.subdomains:
            t = threading.Thread(target=self.check_host,args=(subdomain,))
            t.start()
            t.join()
        return self.live_subdomains


    def extract_domains(self, resp):
        tbl_regex = re.compile('<a name="hostanchor"><\/a>Host Records.*?<table.*?>(.*?)</table>',re.S)
        link_regex = re.compile('<td class="col-md-4">(.*?)<br>',re.S)
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
    x = DNSdumpster("meizu.coms")
    print x.run()