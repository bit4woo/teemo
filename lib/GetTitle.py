# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'



import re
import threading
import Queue
import urllib3
urllib3.disable_warnings()
from netaddr import IPAddress,IPNetwork
from lib import myrequests
req = myrequests

def getSingleTitle(url):
    default_proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "https://127.0.0.1:8080",
    }

    try:
        #response= req.get(url,verify=False)
        response= req.get(url)
        body = response.content
        code = response.status_code
        lastURL = response.url
        #reg_title = re.compile('<title>(.*?)</title>')#不能匹配换行，空格等字符
        reg_title = re.compile('<title>([\s\S]*?)</title>')
        title = reg_title.findall(body)

        if title.__len__()>0:
            result = title[0].strip()
        else:
            result = "Title为空"
    except Exception,e:
        result = "ERROR"
    return result

def getTitle(urlList):
    tmpresult = Queue.Queue()
    threadpool =[]
    for url in urlList:
        t = threading.Thread(target=getSingleTitle,args=url,name=url)
        #print t.getName()
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        threadpool.append(t)

    for t in threadpool:
        t.start()
        while True:
            #判断正在运行的线程数量,如果小于5则退出while循环,
            #进入for循环启动新的进程.否则就一直在while循环进入死循环
            if(len(threading.enumerate()) < 20):
                break
    for t in threadpool:
        t.join() #主线程将等待这个线程，直到这个线程运行结束


    result =set()
    while not tmpresult.empty():
        result.add(tmpresult.get())
    return list(result)



if __name__ =="__main__":

    domainlist = open("domains.txt","r")
    #print getSingleTitle("http://ym.jd.hk.gslb.qianxun.com")
    urllist = []
    for item in domainlist:
        item = item.strip()
        urllist.append("http://"+item)
        urllist.append("https://" + item)

    xxx = getTitle(urllist)

    #iplist = IPNetwork("10.2.2.2/24")
