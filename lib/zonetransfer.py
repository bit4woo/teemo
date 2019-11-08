# !/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import os
import re
import dns.resolver, dns.zone
from lib.log import logger
from lib.common import strip_list
'''
第一步，通过NS记录查询，找到当前域名的权威服务器。
第二步，通过域传送查询，判断当前域的权威服务器是否存在域传送漏洞
值得注意的是：不同的网络环境可能得出完全不一样的结果，一般内网存在该漏洞的几率比较大
'''
class zonetransfer:
    def __init__(self,domain):
        self.domain= domain
        self.nsservers = set()
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
                    self.nsservers.add(str(answer))
        except Exception as e:
            pass
            #print "[-]get ns server error! try: dig %s NS +short" %(domain) , str(e)

    def get_ns_server_nslookup(self):
        try:
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
            dns_servers = strip_list(dns_servers,".")
            self.nsservers = set(list(self.nsservers).extend(dns_servers))
        except Exception as e:
            pass

    def get_ns_server_dig(self):
        if sys.platform != 'win32':
            try:
                dns_servers = os.popen('dig +short NS ' + self.domain).readlines()
                #use command "dig   +short   NS   xxx.com"
                dns_servers = strip_list(dns_servers, ".")
                self.nsservers = set(list(self.nsservers).extend(dns_servers))
            except Exception as e:
                pass

    def axfr_check(self, domain, nsserver):
        logger.info("Checking Server {0}.".format(nsserver))
        try:
            axfr = dns.query.xfr(nsserver, domain, timeout=10, lifetime=10)
            zone = dns.zone.from_xfr(axfr)
            if zone:
                logger.info("[!!!] Nameserver {0} is vulnerable ({1} records)".format(nsserver, len(zone.nodes.items())))
                self.has_zone_transfer += 1
                names = zone.nodes.keys()
                names.sort()
                for n in names:
                    record = zone[n].to_text(n)
                    self.results.append(record)
                    #print(record)
        except Exception as e:
            #print "[get xfr error]", domain, "\t", nsserver, str(e)
            pass

    def check(self):
        logger.info("Doing Zone Transfer Check ...")
        try:
            self.get_ns_server()
            self.get_ns_server_nslookup()
            self.get_ns_server_dig()
        except Exception as e:
            logger.error("Error in {0}: {1}".format(__file__.split('/')[-1],e))
            #return False

        if len(self.nsservers) == 0:
            logger.info("None NS Server found for {0}.".format(self.domain))
            return False
        else:
            logger.info("{0} NS Servers found for {1}.".format(len(self.nsservers),self.domain))
            for _ in self.nsservers:
                self.has_zone_transfer = self.axfr_check(self.domain, _)

            if self.has_zone_transfer != 0 and len(self.results) != 0:
                logger.info("Zone Transfer Detected for {0}".format(self.domain))
                #__file__  current file,the file contains current code.
                fp = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "{0}_zone_transfer.txt".format(self.domain)), "wb")
                fp.writelines("\n".join(self.results))
                fp.close()
                for item in self.results:
                    print(item)
                return True
            if self.has_zone_transfer == 0 or len(self.results) == 0:
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
    #zonetransfer("sf-express.com").axfr_check("sf-express.com","xxxxx.sf.com")
    zonetransfer("sf-express.com").check()