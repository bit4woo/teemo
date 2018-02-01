# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import dns.resolver
import dns.query
from netaddr import IPAddress,IPNetwork
import netaddr
from lib.common import strip_list

def query(domain, record_type='A',server=None):
    resolver = dns.resolver.Resolver()
    if server != None:
        resolver.nameservers = [server]
    ips = []
    try:
        resp = resolver.query(domain, record_type, raise_on_no_answer=False)
        if resp.response.answer:
            tmpip = []
            tmpcname = []
            for i in resp.response.answer:
                for j in i.items:
                    try:
                        #print "{0}   {1}".format(domain,j.address)
                        tmpip.append(j.address)
                    except:# CNAME here
                        #print "{0}   {1}".format(domain,j.to_text())
                        tmpcname.append(j.to_text())
            line ="{0}\t{1}\t{2}".format(domain.ljust(30),", ".join(tmpcname),", ".join(tmpip))
            if tmpip != None: #only collect IPs that don't use CDN （cname）
                ips.extend(tmpip)
            print line
            return ips,line

        # If we don't receive an answer from our current resolver let's
        # assume we received information on nameservers we can use and
        # perform the same query with those nameservers
        if resp.response.additional and resp.response.authority:
            ns = [
                rdata.address
                for additionals in resp.response.additional
                for rdata in additionals.items
            ]
            resolver.nameservers = ns
            return query(resolver, domain, record_type)
        print domain
        return [],domain
    except (dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.exception.Timeout):
        print domain
        return [],domain


def domains2ips(domain_list,server=None):
    IP_list =[]
    lines = []
    domain_list = strip_list(domain_list)
    for domain in set(domain_list):
        try:
            ips,line = query(domain,record_type='A',server=server)
            IP_list.extend(ips)
            lines.append(line)
        except Exception,e:
            print e
            #print domain
    IP_list = list(set(IP_list))
    return IP_list,lines

def iprange(ip_str_list):
    ip_str_list = list(set(ip_str_list))
    ip_str_list= strip_list(ip_str_list)
    #直接获取各个C段
    subnet = set()
    for ip_str in ip_str_list:
        #print ip_str
        ip = IPNetwork(ip_str)
        ip.prefixlen =24
        subnet.add(ip.cidr)
    #print subnet

    #尝试根据IP缩小范围
    smaller_subnet =set()
    for net in subnet:
        tmpIPlist = []
        for ip_str in ip_str_list:
            ip = IPNetwork(ip_str)
            ip.prefixlen = 24
            if ip.cidr == net:#ip属于net
                tmpIPlist.append(ip_str)
        #print tmpIPlist
        if len(tmpIPlist) == 1:
            smaller_subnet.add(tmpIPlist[0])
        elif len(tmpIPlist) >=2:
            smaller = netaddr.spanning_cidr(tmpIPlist)  #type is IPNetwork
            #if smaller != net:
            smaller_subnet.add(smaller)
        elif len(tmpIPlist) ==0:
            print "{0} has no ip".format(net)

    result = []
    for item in smaller_subnet:
        result.append(str(item))
    return result

def smaller_network():
    #list = ['192.168.0.0', '192.168.0.245', '192.168.0.255']
    #list = ['192.168.2.245']
    x = netaddr.spanning_cidr(list)
    print x


if __name__ == "__main__":
    domains = open("C:\Users\jax\Desktop\hrpc (2).txt").readlines()

    x,lines= domains2ips(domains,"172.30.35.35")
    #print x
    #print smaller_network()
    print iprange(x)# problem