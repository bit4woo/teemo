# encoding: utf-8
# 全局配置文件
import random
import sys
sys.dont_write_bytecode = True

##########各种key #############
#这里的都是例子，正确的需要自己申请哟~
Google_CSE_API_Key = "AIzaSyCFyYfbMZwNeObc_wswczgOUbRB0-c2wA0"
Google_CSE_ID = "teemo-1487466194614"

Bing_API_Key = "7fe1cecac425447389c0d3effb73c4f7"

FOFA_USER_EMAIL = "bit4woo@163.com"
FOFA_API_KEY = "4c428ccbf09eeb05590ab842f24c45dd"

SHODAN_API_KEY = "mvqpLKKMMlkyYHUnzVviD0M0C158UV5L"

Censys_API_UID = "fae24d14-fe2a-4e7f-79xx-82f123095908" #just a example
Censys_API_SECRET = "n2MjIKS0RIxdEDQAHRutXz6WDz2yBWBQ"

Whoxy_API_KEY = "43cayya89cb2c3xxxr3d125e2d80de322"

#############reverse lookup option#####################
#域名反查是否交互确认每个联系人和邮箱
Reverse_Email_Confirm = False
Reverse_Company_Name_Confirm = False


#############proxy##################
proxy_switch = 1
#1 = 使用下面的proxy_default_enabled选项
#2 = 全局使用proxy，即所有搜索引擎都使用proxy
#3 = 全局禁用proxy
default_proxies = {
    "http": "http://127.0.0.1:9988",
    "https": "https://127.0.0.1:9988",
}
proxy_default_enabled = [#默认启用代理的搜索引擎
    'search_ask','search_google','search_google_cse','search_duckduckgo','Googlect','ThreatCrowd','DNSdumpster' #类名
    ]


# -------------------------------------------------
# requests 配置项
# -------------------------------------------------

# 超时时间
timeout = 50

# 是否允许URL重定向
allow_redirects = True

#是否校验ssl
allow_ssl_verify =False

# 是否允许继承http Request类的Session支持，在发出的所有请求之间保持cookies。
allow_http_session = True


###########################http header的配置########################
# 是否允许随机User-Agent
allow_random_useragent = True

# 是否允许随机X-Forwarded-For
allow_random_x_forward = False

# 随机HTTP头
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0",
]

# 随机生成User-Agent
def random_useragent(condition=False):
    if condition:
        return random.choice(USER_AGENTS)
    else:
        return USER_AGENTS[0]

# 随机X-Forwarded-For，动态IP
def random_x_forwarded_for(condition=False):
    if condition:
        return '%d.%d.%d.%d' % (random.randint(1, 254),random.randint(1, 254),random.randint(1, 254),random.randint(1, 254))
    else:
        return '8.8.8.8'

# HTTP 头设置
headers = {
    'User-Agent': random_useragent(allow_random_useragent),
    'X_FORWARDED_FOR': random_x_forwarded_for(allow_random_x_forward),
    'Referer' : 'http://www.baidu.com',
}


#################subdomainbrute options#############################
subnamefile = "subnames.txt"   #subnames_full.txt
ignore_intranet = False
threads = 100
full_scan = True
