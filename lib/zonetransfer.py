# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import os
import re
import dns.resolver, dns.zone
from lib.log import logger

class zonetransfer:
    def __init__(self,domain):
        self.domain= domain
        self.nsservers = []
        self.results =[]
        self.has_zone_transfer = 0


    def get_ns_server(self):
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            resolver.lifetime = 10

            # 使用阿里DNS服务器，效果不咋滴
            #resolver.nameservers = ["223.5.5.5", "223.6.6.6"]

            answers = resolver.query(self.domain, "NS")
            if answers:
                for answer in answers:
                    #print answer
                    self.nsservers.append(str(answer))
        except Exception, e:
            pass
            #print "[-]get ns server error! try: dig %s NS +short" %(domain) , str(e)

    def get_ns_server_nslookup(self):
        #result = os.system("nslookup -type=ns {0}".format(domain))
        result = os.popen('nslookup -type=ns ' + self.domain).read()
        #print result
        #其实域名后是否有点对axfr查询无影响
        '''
        if sys.platform == 'win32':
            dns_servers = re.findall('nameserver = (.*?)\n', result)
        else:
            dns_servers = re.findall('nameserver = (.*?)\.\n', result)
        '''
        dns_servers = re.findall('nameserver = (.*?)\n', result)
        self.nsservers.extend(dns_servers)

    def axfr_check(self, domain, nsserver):
        try:
            zone = dns.zone.from_xfr(dns.query.xfr(str(nsserver), domain, timeout=5, lifetime=10))
            if zone:
                self.has_zone_transfer += 1
                names = zone.nodes.keys()
                names.sort()
                for n in names:
                    record = zone[n].to_text(n)
                    self.results.append(record)
                    print record
        except Exception, e:
            #print "[get xfr error]", domain, "\t", nsserver, str(e)
            pass

    def check(self):
        logger.info("Doing Zone Transfer Check ...")
        try:
            self.get_ns_server()
            self.get_ns_server_nslookup()
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            return False

        if len(self.nsservers) == 0:
            logger.info("None NS Server found for {0}.".format(self.domain))
            return False
        else:
            for _ in self.nsservers:
                has_zone_transfer = self.axfr_check(self.domain, _)

            if has_zone_transfer != 0 and len(self.results) != 0:
                logger.info("Zone Transfer Detected for {0}".format(self.domain))
                #__file__  current file,the file contains current code.
                fp = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "{0}_zone_transfer.txt".format(self.domain)), "wb")
                fp.writelines(self.results)
                fp.close()
                for item in self.results:
                    print item
                return True
            if has_zone_transfer == 0 or len(self.results) == 0:
                logger.info("Zone Transfer False")
                return False


if __name__ == '__main__':
    '''
    a = get_ns_server("meizu.com")
    b = get_ns_server_nslookup("meizu.com")
    print a
    print b

    for _ in ["ns1.as6453.net"]:
        z= axfr_check("bf",_)
    '''
    zonetransfer("insecuredns.com").check()
