# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import dns.resolver
import dns.query
from netaddr import IPAddress,IPNetwork
import netaddr
from lib.common import strip_list

def query(domain, record_type='A'):
    resolver = dns.resolver.Resolver()
    ips = []
    try:
        resp = resolver.query(domain, record_type, raise_on_no_answer=False)
        if resp.response.answer:
            for i in resp.response.answer:
                for j in i.items:
                    try:
                        print "{0}   {1}".format(domain,j.address)
                        ips.append(j.address)
                    except:# CNAME here
                        print "{0}   {1}".format(domain,j.to_text())
            return ips

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

        return []
    except (dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.exception.Timeout):
        return []



def get_class_c_network(ip_str_list):
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
            if ip.cidr == net:
                tmpIPlist.append(ip_str)
        #print tmpIPlist
        if len(tmpIPlist) == 1:
            smaller_subnet.add(tmpIPlist[0])
        elif len(tmpIPlist) >=2:
            smaller = netaddr.spanning_cidr(tmpIPlist)  #type is IPNetwork
            if smaller != net:
                smaller_subnet.add(smaller)
        elif len(tmpIPlist) ==0:
            print "{0} has no ip".format(net)

    result = []
    for item in smaller_subnet:
        result.append(str(item))
    return result

def smaller_network(ip_str_list):
    x = netaddr.spanning_cidr(['192.168.0.0', '192.168.2.245', '192.168.2.255'])
    print x


def get_IP_range(domain_list):
    IP_list =[]
    for domain in domain_list:
        try:
            IP_list.extend(query(domain))
        except Exception,e:
            print e
            print domain
    IP_list = list(set(IP_list))

    return get_class_c_network(IP_list)

if __name__ == "__main__":

    #print query("baidu.com")
    iplist = open("C:\Users\jax\Desktop\ips.txt").readlines()
    #print iplist
    fp = open("tmp.txt", "wb")
    x = get_IP_range(["baidu.com"])
    fp.writelines("\n".join(x))
