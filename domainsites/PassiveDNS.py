__author__ = 'bit4'
#wydomain
import multiprocessing
import threading
import urlparse
import requests
import re


class PassiveDNS(multiprocessing.Process):
    def __init__(self, domain, proxy=None):
        self.base_url = 'http://ptrarchive.com/tools/search.htm?label={domain}'
        #self.domain = urlparse.urlparse(domain).netloc
        self.domain = domain
        self.subdomains = []
        self.session = requests.Session()
        self.engine_name = "PassiveDNS"
        multiprocessing.Process.__init__(self)
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
        print "[-] Searching now in %s.." %(self.engine_name)
        return

    def req(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        }

        try:
            resp = self.session.get(url, headers=headers, timeout=self.timeout)
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

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.req(url)
        self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        link_regx = re.compile('<td>(.*?)</td>')
        try:
            links = link_regx.findall(resp)
            for link in links:
                if self.domain not in link:
                    continue
                subdomain = link[:link.find('[')].strip()
                if subdomain not in self.subdomains and subdomain != self.domain and subdomain.endswith(self.domain):
                    #if verbose:
                    #   print "%s%s: %s%s"%(R, self.engine_name, W, subdomain)
                    self.subdomains.append(subdomain.strip())
        except Exception as e:
            pass

if __name__ == "__main__":
    x = PassiveDNS("meizu.com","https://127.0.0.1:9999")
    print x.run()