# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
import urllib
import urllib2
import base64
import re
import time
import random
import simplejson
import config


def useAPI(): #超过数量需要付费;不付费的情况下只能获取100个结果
    email = config.FOFA_USER_EMAIL
    key= config.FOFA_API_KEY

    if email is "":
        email = raw_input("Please Input Email:")
    if key is "":
        key = raw_input("Please input key:")

    auth_url = "https://fofa.so/api/v1/info/my?email={0}&key={1}".format(email,key)
    #print auth_url
    response = urllib.urlopen(auth_url)
    #print response.read()

    query = base64.b64encode(raw_input("Please input query:"))#"Powered+by+vancheer"
    request = "https://fofa.so/api/v1/search/all?email={0}&key={1}&qbase64={2}".format(email,key,query)

    response = urllib.urlopen(request)

    resp = response.readlines()[0]
    resp = simplejson.loads(resp)
    #print resp
    if resp["error"] == None:
        #print len(resp['results'])
        for item in resp['results']:
            if item[0].startswith("https"):
                pass
            else:
                item[0] = "http://"+item[0]
            print "{0} {1}".format(item[0],item[1])
        if resp['size'] >=100:
            print "{0} items found! just 100 get....".format(resp['size'])
    else:
        exit(0)

def usecookie():

    url = raw_input("Please Input URL Or Query Key Words:")
    if url.startswith("https://fofa.so/result?"):
        #https://fofa.so/result?q=domain%3Dwolaidai.com&qbase64=ZG9tYWluPXdvbGFpZGFpLmNvbQ%3D%3D
        pass
    else:
        url = "https://fofa.so/result?q={0}&qbase64={1}".format(url,base64.b64encode(url))

    cookie = raw_input("Please Input cookie:")
    if "_fofapro_ars_session=" in cookie:
        pass
    else:
        cookie = "_fofapro_ars_session="+cookie
    print cookie
    li = range(1,30)
    random.shuffle(li)#to use page number not in order可以尝试乱序，看看能不能绕过频繁请求的检测
    for i in li:
        url = url.replace(" ","")+'&page='+str(i)
        #print url
        request = urllib2.Request(url)
        request.add_header('Cookie', cookie)
        response = urllib2.urlopen(request)
        html = response.read()
        #print html
        urllist = findLinks(html)
        for item in urllist:
            print item
        if "next_page" in html:
            time.sleep(random.randint(3,10))
            continue
        else:
            break

def findLinks(htmlString):
    links = re.compile("<a target=\"_blank\" href=\"(.+?)\"")
    return links.findall(htmlString) #list


def usecookietest():
    request = urllib2.Request('https://fofa.so/result?q=%22Powered+by+vancheer%22&qbase64=IlBvd2VyZWQgYnkgdmFuY2hlZXIi&page=4')
    request.add_header('Cookie', 'locale=zh-CN; _fofapro_ars_session=330b83bee72e84fbfs2eeb1471d2e6643')
    response = urllib2.urlopen(request)
    print response.read()

if __name__ == "__main__":
    while True:
        method = raw_input("Use API or Cookie:(1.API 2.Cookie[default])")
        if method =="1":
            useAPI()
            break
        elif method == "2" or method== "":
            usecookie()
            break
        else:
            print "error options"
            continue
