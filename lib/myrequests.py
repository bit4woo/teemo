# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import config
from lib.log import logger
import traceback
import requests
import requests as __requests__

requests.adapters.DEFAULT_RETRIES = 2 #设置失败时的重新请求次数
try:
    import urllib3
    urllib3.disable_warnings()
except:
    pass
'''
这个类的主要目的是对requests的参数都设置一个默认的值，调用时如果没有参数参数，就使用config中的默认值。
如果有传入，就是用传入的值。这样，可以在config中全局控制，也可以在具体的调用时定制化控制。
当然，在具体调用时也可以通过读取config进行修改然后在传入。

使用traceback.print_exc()，是为了让这个类和元素requests的表现一模一样。
'''

if config.allow_http_session:
    requests = requests.Session()

def get(url,stream=False,allow_redirects=config.allow_redirects,headers=config.headers,
        cookies = None,timeout=config.timeout,proxies = None,verify= config.allow_ssl_verify):

    try:
        result = requests.get(url,
            stream=stream,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies = cookies,
            timeout=timeout,
            proxies=proxies,
            verify=verify)
        return result
    except Exception, e:
        raise e#这个信息会被调用它的代码的try ..except捕获，而不会直接在这里输出错误信息，让程序输出更工整
        #logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))

        # return empty requests object
        #return __requests__.models.Response()

def post(url, data, stream=False, allow_redirects=config.allow_redirects, headers=config.headers,cookies = None,
         timeout=config.timeout, proxies = None, verify =config.allow_ssl_verify):
    """ data = {'key1': 'value1', 'key2': 'value2'} """
    try:
        result = requests.post(url,
            data=data,
            stream=stream,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies = cookies,
            timeout=timeout,
            proxies=proxies,
            verify=verify)
        return result
    except Exception, e:
        raise e
        #traceback.print_exc()
        #logger.error("Error in {0}: {1}".format(__file__.split('/')[-1], e))
        # return empty requests object
        #return __requests__.models.Response()

if __name__ == "__main__":
    print type(get("http://www.baidu.com:8000",timeout=1).content)
    #requests.get("http://www.baidu.com:8000",timeout=1)