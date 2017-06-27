# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
import string
import httplib
import sys
from lib import myparser
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
        self.q = []

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
        self.q = self.get_hostnames() # how to receive emails.
        print "[-] {0} found {1} domains".format(self.engine_name, len(self.q))
        return self.q
