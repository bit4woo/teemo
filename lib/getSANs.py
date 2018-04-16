# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import urlparse
import os,sys
import ssl,socket
import datetime
import argparse

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


def parser_error(errmsg):
    print ("Usage: python "+sys.argv[0]+" [Options] use -h for help")
    sys.exit()

def parse_args(): #optparse模块从2.7开始废弃，建议使用argparse
    parser = argparse.ArgumentParser(epilog = "\tExample: \r\npython {0} -d baidu.com\r\npython {0} -f domain.txt".format(sys.argv[0]))
    parser.error = parser_error #or a function name
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--domain', help="Domain name", required=True)
    parser.add_argument('-f', '--file', help='file that contains domain list')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.domain:
        domains =  getSANs(domain=args.domain)
        print ("\r\n".join(domains))
    elif args.file:
        main(args.file)
