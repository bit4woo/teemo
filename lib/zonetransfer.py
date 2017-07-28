# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import os
import re
import dns.resolver, dns.zone

def get_ns_server(domain):
    ns_servers = []
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 10

        # 使用阿里DNS服务器，效果不咋滴
        #resolver.nameservers = ["223.5.5.5", "223.6.6.6"]

        answers = resolver.query(domain, "NS")
        if answers:
            for answer in answers:
                #print answer
                ns_servers.append(str(answer))
    except Exception, e:
        print "[-]get ns server error! try: dig %s NS +short" %(domain) , str(e)
    return ns_servers #域名末尾有点

def get_ns_server_nslookup(domain):
    #result = os.system("nslookup -type=ns {0}".format(domain))
    result = os.popen('nslookup -type=ns ' + domain).read()
    #print result
    #其实域名后是否有点对axfr查询无影响
    '''
    if sys.platform == 'win32':
        dns_servers = re.findall('nameserver = (.*?)\n', result)
    else:
        dns_servers = re.findall('nameserver = (.*?)\.\n', result)
    '''
    dns_servers = re.findall('nameserver = (.*?)\n', result)
    return dns_servers

def axfr_check(domain, nsserver):
    has_zone_transfer = False
    results = []
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(str(nsserver), domain, timeout=5, lifetime=10))
        if zone:
            has_zone_transfer = True
            names = zone.nodes.keys()
            names.sort()
            for n in names:
                record = zone[n].to_text(n)
                results.append(record)
                print record
    except Exception, e:
        #print "[get xfr error]", domain, "\t", nsserver, str(e)
        pass
    return has_zone_transfer,results

def check(domain):
    try:
        nsserver = get_ns_server(domain)
    except:
        try:
            nsserver = get_ns_server_nslookup()
        except:
            pass
    finally:
        nsserver = []

    if nsserver == "None":
        print "None NS Server found for {0}".format(domain)
    else:
        for _ in nsserver:
            has_zone_transfer,results = axfr_check(domain, _)
            fp = open(".\\output\\{0}_zone_transfer.txt".format(_),"wb")
            if has_zone_transfer == True:
                print "Zone Transfer Detected for {0}".format(_)
                for item in results:
                    print item
                    fp.write(item)
            else:
                pass

if __name__ == '__main__':
    '''
    a = get_ns_server("meizu.com")
    b = get_ns_server_nslookup("meizu.com")
    print a
    print b
    '''

    for _ in ["ns1.as6453.net"]:
        z= axfr_check("bf",_)
