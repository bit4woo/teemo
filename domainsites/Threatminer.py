__author__ = 'bit4'
#wydomain
import multiprocessing
import threading
import urlparse
from lib.common import *

class Threatminer(multiprocessing.Process):
    def __init__(self, domain, proxy=None):
        #self.domain = urlparse.urlparse(domain).netloc
        self.domain = domain
        self.subdomains = []
        self.engine_name = "Threatminer"
        multiprocessing.Process.__init__(self)
        self.q = []
        self.timeout = 25
        self.print_banner()
        self.website = "https://www.threatminer.org"
        return

    def print_banner(self):
        print "[-] Searching now in %s.." %(self.engine_name)
        return

    def run(self):
        try:
            url = "{0}/getData.php?e=subdomains_container&q={1}&t=0&rt=10&p=1".format(self.website, self.domain)
            # content = curl_get_content(url).get('resp')
            content = http_request_get(url).content

            _regex = re.compile(r'(?<=<a href\="domain.php\?q=).*?(?=">)')
            for sub in _regex.findall(content):
                if is_domain(sub):
                    self.q.append(sub)

            self.q = list(set(self.q))
        except Exception as e:
            logging.info(str(e))

        print "[-] {0} found {1} domains".format(self.engine_name, len(self.q))
        return self.q

if __name__ == "__main__":
    x = Threatminer("meizu.com","https://127.0.0.1:9999")
    print x.run()