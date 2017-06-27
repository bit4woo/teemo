# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'


import shodan
import csv
import datetime
import sys
import urllib
import socket
import config
#connect to shodan
SHODAN_API_KEY = config.SHODAN_API_KEY
api = shodan.Shodan(SHODAN_API_KEY)


now = datetime.datetime.now()
datestr = now.strftime("%Y%m%d")
#print datestr
socket.setdefaulttimeout(2)

if len(sys.argv) == 1:
        print 'Usage: %s <search query>' % sys.argv[0]
        sys.exit(1)
else:
        query = ' '.join(sys.argv[1:])
        filename = '_'.join(sys.argv[1:])
        filename = filename+'_'+datestr+'.csv'
        #

try:
        # Search Shodan
        results = api.search(query)
        writer = csv.writer(file(filename,'wb'))
        # Show the results
        print 'Results found: %s' % results['total']
        for result in results['matches']:
                #print 'IP: %s' % result['ip_str']
                #print result['data']
                #print ''
                #print result
                #print tuple(result)
                #result是一个字典。
                print '#######################\n'
                resultlist = tuple([result['ip_str'],result['port']])
                url = 'http://'+result['ip_str']+":"+str(result['port'])+'/index.php?cperpage=1'
                try:
                    response = urllib.urlopen(url)
                    if response.code == 200 and 'WordPress' in response.read():
                        print url
                    #print resultlist
                except Exception:
                    pass
                writer.writerow(resultlist)
except shodan.APIError, e:
        print 'Error: %s' % e







'''
# Lookup the host
host = api.host('217.140.75.46')

# Print general info
print """
        IP: %s
        Organization: %s
        Operating System: %s
""" % (host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a'))

# Print all banners
for item in host['data']:
        print """
                Port: %s
                Banner: %s

        """ % (item['port'], item['data'])
'''
