# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from config import *
import subprocess
import logging
import requests as __requests__


import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

if allow_http_session:
    requests = requests.Session()

def http_request_get(url, body_content_workflow=False, allow_redirects=allow_redirects, custom_cookie="",custom_referer="", proxies = None):
    try:
        if custom_cookie:
            headers['Cookie']= custom_cookie
        if custom_referer:
            headers['Referer'] = custom_referer
        result = requests.get(url,
            stream=body_content_workflow,
            headers=headers,
            timeout=timeout,
            proxies=proxies,
            allow_redirects=allow_redirects,
            verify=allow_ssl_verify)
        return result
    except Exception, e:
        # return empty requests object
        return __requests__.models.Response()

def http_request_post(url, payload, body_content_workflow=False, allow_redirects=allow_redirects, custom_cookie="", custom_referer="",proxies = None):
    """ payload = {'key1': 'value1', 'key2': 'value2'} """
    try:
        if custom_cookie:
            headers['Cookie']= custom_cookie
        if custom_referer:
            headers['Referer'] = custom_referer
        result = requests.post(url,
            data=payload,
            headers=headers,
            stream=body_content_workflow,
            timeout=timeout,
            proxies=proxies,
            allow_redirects=allow_redirects,
            verify=allow_ssl_verify)
        return result
    except Exception, e:
        # return empty requests object
        return __requests__.models.Response()

def curl_get_content(url):
    try:
        cmdline = 'curl "{url}"'.format(url=url)
        logging.info("subprocess call curl: {}".format(url))
        run_proc = subprocess.Popen(
            cmdline,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        (stdoutput,erroutput) = run_proc.communicate()
        response = {
            'resp': stdoutput.rstrip(),
            'err': erroutput.rstrip(),
        }
        return response
    except Exception as e:
        pass


