# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import urlparse
import os,sys
import ssl,socket
import datetime

'''
pip install pysocks
socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9988)
'''
def getSANs(domain,port=443,host_match=True):
    domains = []
    try:
        ctx = ssl.create_default_context()
        #s = ctx.wrap_socket(socket.socket(), server_hostname="google.com")
        s = ctx.wrap_socket(socket.socket(), server_hostname=domain)
        s.connect((domain, port))
        cert = s.getpeercert()
        #print cert
        SANs = cert['subjectAltName']
        for SAN in SANs:
            domains.append(SAN[-1])
    except ssl.CertificateError,e:
        print(e)
        if "doesn't match either of " in str(e) and host_match == False:
            index =  str(e).index("doesn't match either of ")+len("doesn't match either of ")
            e = str(e)[index:-1]
            domains = [x.replace("'","").strip() for x in e.split(",")]
    except Exception,e:
        print(e)
    return domains


def main(domainfile,outputfile=None):
    if outputfile ==None:
        now = datetime.datetime.now()
        timestr = now.strftime("-%Y-%m-%d-%H-%M")
        outputfile = "related-domain" + timestr + ".txt"
        outputfile= os.path.join(os.path.dirname(__file__), "..","output", outputfile)
    if  os.path.exists(domainfile):
        result = []
        lines = open(domainfile,"r").readlines()
        for line in lines:
            try:
                if line.startswith("https://"):
                    domain = urlparse.urlparse(line).hostname
                else:
                    domain = line
                result.extend(getSANs(domain.strip(), 443, False))
            except Exception,e:
                print(e)
        result = list(set(result))
        open(outputfile,"w").writelines("\n".join(result))
    else:
        print("file not found")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "{0} domain file".format(sys.argv[0])
    else:
        main(sys.argv[1])
