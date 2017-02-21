__author__ = 'bit4'

#wydomain

import multiprocessing
import threading
import urlparse
from lib.common import *
from lib.captcha import *


class Sitedossier(multiprocessing.Process):
    def __init__(self, domain, proxy=None):
        #self.domain = urlparse.urlparse(domain).netloc
        self.domain = domain
        self.subdomains = []
        self.session = requests.Session()
        self.engine_name = "Sitedossier"
        multiprocessing.Process.__init__(self)
        self.q = []
        self.timeout = 25
        self.print_banner()
        self.captcha = Captcha()
        return

    def print_banner(self):
        print "[-] Searching now in %s.." %(self.engine_name)
        return

    def run(self):
        try:
            url = 'http://www.sitedossier.com/parentdomain/{0}'.format(self.domain)
            r = self.get_content(url)
            self.parser(r)
            self.q = list(set(self.q))
        except Exception, e:
            logging.info(str(e))

        print "[-] {0} found {1} domains".format(self.engine_name, len(self.q))
        return self.q

    def get_content(self, url):
        logging.info('request: {0}'.format(url))
        r = http_request_get(url).text
        if self.human_act(r) is True:
            return r
        else:
            self.get_content(url)

    def parser(self, response):
        npage = re.search('<a href="/parentdomain/(.*?)"><b>Show', response)
        if npage:
            for sub in self.get_subdomain(response):
                self.q.append(sub)
            nurl = 'http://www.sitedossier.com/parentdomain/{0}'.format(npage.group(1))
            response = self.get_content(nurl)
            self.parser(response)
        else:
            for sub in self.get_subdomain(response):
                self.q.append(sub)

    def get_subdomain(self, response):
        domain = re.compile(r'(?<=<a href\=\"/site/).*?(?=\">)')
        for sub in domain.findall(response):
            yield sub

    def human_act(self, response):
        if 'auditimage' in response or 'blacklisted' in response:
            imgurl = self.get_audit_img(response)
            if imgurl is not None:
                ret = self.captcha.verification(imgurl)
                if ret.has_key('Result'):
                    self.audit(ret['Result'])
                    return True
                else:
                    raise Exception("captcha_verification_is_empty")
            else:
                raise Exception("audit_img_is_empty")
        else:
            return True

    def audit(self, code):
        payload = {'w':code}
        url = 'http://www.sitedossier.com/audit'
        r = http_request_post(url, payload=payload)

    def get_audit_img(self, response):
        auditimg = re.compile(r'(?<=<img src\=\"/auditimage/).*?(?=\?" alt="Please)')
        imgurl = auditimg.findall(response)[0:]
        if len(imgurl) >= 1:
            imgurl = 'http://www.sitedossier.com/auditimage/{0}'.format(imgurl[0])
            return imgurl
        else:
            return None

    def __str__(self):
        handler = lambda e: str(e)
        return json.dumps(self, indent=2, default=handler)

if __name__ == "__main__":
    x = Sitedossier("meizu.com","https://127.0.0.1:9999")
    print x.run()