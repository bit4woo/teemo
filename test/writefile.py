#coding:utf-8
subdomains = [u'inforum.meizu.com', u'csc.meizu.com', u'member.meizu.com', u'care.meizu.com', u'mail.meizu.com', u'booking.meizu.com', u'event.meizu.com', u'ros.meizu.com', u'flymebbs.meizu.com', u'app.meizu.com', u'hr.meizu.com', u'detail.mall.meizu.com', u'service.meizu.com', u'406.meizu.com', u'en.meizu.com', u'www.meizu.com', u'oa.meizu.com', u'rms.meizu.com', u'-www.meizu.com', u'-gamebbs.meizu.com', u'eva.meizu.com', u'53kf2.meizu.com', u'sec.meizu.com', u'm.meizu.com', u'wanmei.meizu.com', u'detail.meizu.com', u'bbs.meizu.com', u'buying.meizu.com', u'flyme.meizu.com', u'retail.meizu.com', u'wan.meizu.com', u'mcycle.mall.meizu.com', u'www2.res.meizu.com', u'A8m.meizu.com', u'mall.meizu.com', u'e.meizu.com', u'life.meizu.com', u'developer.meizu.com', u'store.meizu.com', u'2Fstore.meizu.com', u'sync.meizu.com', u'forum.meizu.com', u'kf2.meizu.com', u'findphone.meizu.com', u'gamebbs.meizu.com', u'lifekit.meizu.com', u'pay.meizu.com', u'mcycle.meizu.com', u'hd.meizu.com']
emails = ['a','b']
def write_file(filename, subdomains):
    #saving subdomains results to output file
    with open(str(filename), 'wb') as f:
        for subdomain in subdomains:
            f.write(subdomain+"\r\n")



if subdomains is not None:
    subdomains = sorted(subdomains)
    emails = sorted(emails)
    subdomains.extend(emails)
    print type(subdomains)#extend 后就变成了nonetype ,why
    if True:
        write_file("xxx", subdomains)
    else:
        write_file(domain, subdomains)

if __name__ == "__main__":
    fp = open("test","w")
    fp.writelines("\n".join(subdomains).decode("utf-8"))