# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import httplib
from lib import myparser
from lib.log import logger
# to do :return emails

class Pgpsearch:

    def __init__(self, word, proxy = None):
        self.word = word
        self.results = ""
        self.server = "pgp.mit.edu"
        #self.server = "pgp.rediris.es:11371" Not  working at the moment
        self.hostname = "pgp.mit.edu"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.engine_name = "PGP"
        self.domain_name = []
        self.smiliar_domain_name = []
        self.email = []
        self.print_banner()

    def print_banner(self):
        logger.info("Searching now in {0}..".format(self.engine_name))
        return

    def process(self):
        h = httplib.HTTP(self.server)
        h.putrequest('GET', "/pks/lookup?search=" + self.word + "&op=index")
        h.putheader('Host', self.hostname)
        h.putheader('User-agent', self.userAgent)
        h.endheaders()
        returncode, returnmsg, headers = h.getreply()
        print returncode
        print returnmsg
        self.results = h.getfile().read()

    def get_emails(self):
        rawres = myparser.parser(self.results, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.results, self.word)
        return rawres.hostnames()
    def run(self):
        self.domain_name = self.get_hostnames() # how to receive emails.
        self.email = self.get_emails()
        logger.info("{0} found {1} domains and {2} emails".format(self.engine_name, len(self.domain_name), len(self.email)))
        return self.domain_name,self.smiliar_domain_name,self.email

if __name__ == "__main__":
    x= Pgpsearch("meizu.com")
    print x.run()