#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    subDomainsBrute 1.0.6
    A simple and fast sub domains brute tool for pentesters
    my[at]lijiejie.com (http://www.lijiejie.com)
"""

import gevent
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from gevent.queue import PriorityQueue
import sys
import re
import dns.resolver
import time
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib.consle_width import getTerminalSize
import config

class SubNameBrute:
    def __init__(self, target, subdomainfile=None):
        self.start_time = time.time()
        self.target = target.strip()
        self.ignore_intranet = config.ignore_intranet
        self.scan_count = self.found_count = 0
        self.console_width = getTerminalSize()[0] - 2
        self.threads = config.threads
        self.resolvers = [dns.resolver.Resolver(configure=False) for _ in range(self.threads)]
        for _ in self.resolvers:
            _.lifetime = _.timeout = 10.0
        self.print_count = 0
        self.STOP_ME = False
        try:
            self.full_scan = config.full_scan
        except:
            self.full_scan = False
        self.subdomainfile = subdomainfile if subdomainfile != None else config.subnamefile
        self.basedir = os.path.dirname(os.path.dirname(__file__)) #Teemo home dir
        self._load_dns_servers()
        self._load_next_sub()
        self.queue = PriorityQueue()
        self.priority = 0
        self._load_sub_names()
        self.ip_dict = {}
        self.found_subs = set()
        self.ex_resolver = dns.resolver.Resolver(configure=False)
        self.ex_resolver.nameservers = self.dns_servers
        self.result_lines= []
        self.result_domains = []
        self.result_ips = []


    def _load_dns_servers(self):
        print '[+] Validate DNS servers ...'
        self.dns_servers = []
        pool = Pool(30)
        filename = os.path.join(self.basedir,"dict","dns_servers.txt")
        for server in open(filename).xreadlines():
            server = server.strip()
            if server:
                pool.apply_async(self._test_server, (server,))
        pool.join()

        self.dns_count = len(self.dns_servers)
        sys.stdout.write('\n')
        print '[+] Found %s available DNS Servers in total' % self.dns_count
        if self.dns_count == 0:
            print '[ERROR] No DNS Servers available.'
            sys.exit(-1)

    def _test_server(self, server):
        resolver = dns.resolver.Resolver()
        resolver.lifetime = resolver.timeout = 10.0
        try:
            resolver.nameservers = [server]
            answers = resolver.query('public-dns-a.baidu.com')    # test lookup a existed domain
            if answers[0].address != '180.76.76.76':
                raise Exception('incorrect DNS response')
            try:
                resolver.query('test.bad.dns.lijiejie.com')    # Non-existed domain test
                with open('bad_dns_servers.txt', 'a') as f:
                    f.write(server + '\n')
                self._print_msg('[+] Bad DNS Server found %s' % server)
            except:
                self.dns_servers.append(server)
            self._print_msg('[+] Check DNS Server %s < OK >   Found %s' % (server.ljust(16), len(self.dns_servers)))
        except:
            self._print_msg('[+] Check DNS Server %s <Fail>   Found %s' % (server.ljust(16), len(self.dns_servers)))

    def _load_sub_names(self):
        self._print_msg('[+] Load sub names ...')
        if self.full_scan and self.subdomainfile == 'subnames.txt':
            _file = os.path.join(self.basedir,'dict','subnames_full.txt')
        else:
            if os.path.exists(self.subdomainfile):
                _file = self.subdomainfile
            elif os.path.exists(os.path.join(self.basedir,'dict',self.subdomainfile)):
                _file = os.path.join(self.basedir,'dict',self.subdomainfile)
            else:
                self._print_msg('[ERROR] Names file not exists: %s' % self.subdomainfile)
                exit(-1)

        normal_lines = []
        wildcard_lines = []
        wildcard_list = []
        regex_list = []
        lines = set()
        with open(_file) as f:
            for line in f.xreadlines():
                sub = line.strip()
                if not sub or sub in lines:
                    continue
                lines.add(sub)

                if sub.find('{alphnum}') >= 0 or sub.find('{alpha}') >= 0 or sub.find('{num}') >= 0:
                    wildcard_lines.append(sub)
                    sub = sub.replace('{alphnum}', '[a-z0-9]')
                    sub = sub.replace('{alpha}', '[a-z]')
                    sub = sub.replace('{num}', '[0-9]')
                    if sub not in wildcard_list:
                        wildcard_list.append(sub)
                        regex_list.append('^' + sub + '$')
                else:
                    normal_lines.append(sub)
        pattern = '|'.join(regex_list)
        if pattern:
            _regex = re.compile(pattern)
            if _regex:
                for line in normal_lines[:]:
                    if _regex.search(line):
                        normal_lines.remove(line)

        for item in normal_lines:
            self.priority += 1
            self.queue.put((self.priority, item))

        for item in wildcard_lines:
            self.queue.put((88888888, item))

    def _load_next_sub(self):
        self._print_msg('[+] Load next level subs ...')
        self.next_subs = []
        _set = set()
        _file = os.path.join(self.basedir,'dict','next_sub.txt') if not self.full_scan else os.path.join(self.basedir,'dict','next_sub_full.txt')
        with open(_file) as f:
            for line in f:
                sub = line.strip()
                if sub and sub not in self.next_subs:
                    tmp_set = {sub}
                    while len(tmp_set) > 0:
                        item = tmp_set.pop()
                        if item.find('{alphnum}') >= 0:
                            for _letter in 'abcdefghijklmnopqrstuvwxyz0123456789':
                                tmp_set.add(item.replace('{alphnum}', _letter, 1))
                        elif item.find('{alpha}') >= 0:
                            for _letter in 'abcdefghijklmnopqrstuvwxyz':
                                tmp_set.add(item.replace('{alpha}', _letter, 1))
                        elif item.find('{num}') >= 0:
                            for _letter in '0123456789':
                                tmp_set.add(item.replace('{num}', _letter, 1))
                        elif item not in _set:
                            _set.add(item)
                            self.next_subs.append(item)

    def _print_msg(self, _msg=None, _found_msg=False):
        if _msg is None:
            self.print_count += 1
            if self.print_count < 100:
                return
            self.print_count = 0
            msg = '%s Found| %s Groups| %s scanned in %.1f seconds' % (
                self.found_count, self.queue.qsize(), self.scan_count, time.time() - self.start_time)
            sys.stdout.write('\r' + ' ' * (self.console_width - len(msg)) + msg)
        elif _msg.startswith('[+] Check DNS Server'):
            sys.stdout.write('\r' + _msg + ' ' * (self.console_width - len(_msg)))
        else:
            sys.stdout.write('\r' + _msg + ' ' * (self.console_width - len(_msg)) + '\n')
            if _found_msg:
                msg = '%s Found| %s Groups| %s scanned in %.1f seconds' % (
                    self.found_count, self.queue.qsize(), self.scan_count, time.time() - self.start_time)
                sys.stdout.write('\r' + ' ' * (self.console_width - len(msg)) + msg)
        sys.stdout.flush()

    @staticmethod
    def is_intranet(ip):
        ret = ip.split('.')
        if len(ret) != 4:
            return True
        if ret[0] == '10':
            return True
        if ret[0] == '172' and 16 <= int(ret[1]) <= 32:
            return True
        if ret[0] == '192' and ret[1] == '168':
            return True
        return False

    def put_item(self, item):
        num = item.count('{alphnum}') + item.count('{alpha}') + item.count('{num}')
        if num == 0:
            self.priority += 1
            self.queue.put((self.priority, item))
        else:
            self.queue.put((self.priority + num * 10000000, item))

    def _scan(self, j):
        self.resolvers[j].nameservers = [self.dns_servers[j % self.dns_count]]
        while not self.queue.empty():
            try:
                item = self.queue.get(timeout=1.0)[1]
                self.scan_count += 1
            except:
                break
            self._print_msg()
            try:
                if item.find('{alphnum}') >= 0:
                    for _letter in 'abcdefghijklmnopqrstuvwxyz0123456789':
                        self.put_item(item.replace('{alphnum}', _letter, 1))
                    continue
                elif item.find('{alpha}') >= 0:
                    for _letter in 'abcdefghijklmnopqrstuvwxyz':
                        self.put_item(item.replace('{alpha}', _letter, 1))
                    continue
                elif item.find('{num}') >= 0:
                    for _letter in '0123456789':
                        self.put_item(item.replace('{num}', _letter, 1))
                    continue
                elif item.find('{next_sub}') >= 0:
                    for _ in self.next_subs:
                        self.queue.put((0, item.replace('{next_sub}', _, 1)))
                    continue
                else:
                    sub = item

                if sub in self.found_subs:
                    continue

                cur_sub_domain = sub + '.' + self.target
                _sub = sub.split('.')[-1]
                try:
                    answers = self.resolvers[j].query(cur_sub_domain)
                except dns.resolver.NoAnswer, e:
                    answers = self.ex_resolver.query(cur_sub_domain)

                if answers:
                    self.found_subs.add(sub)
                    ips = ', '.join(sorted([answer.address for answer in answers]))
                    if ips in ['1.1.1.1', '127.0.0.1', '0.0.0.0']:
                        continue

                    if self.ignore_intranet and SubNameBrute.is_intranet(answers[0].address):
                        continue

                    try:
                        self.scan_count += 1
                        answers = self.resolvers[j].query(cur_sub_domain, 'cname')
                        cname = answers[0].target.to_unicode().rstrip('.')
                        if cname.endswith(self.target) and cname not in self.found_subs:
                            self.found_subs.add(cname)
                            cname_sub = cname[:len(cname) - len(self.target) - 1]    # new sub
                            self.queue.put((0, cname_sub))

                    except:
                        pass

                    if (_sub, ips) not in self.ip_dict:
                        self.ip_dict[(_sub, ips)] = 1
                    else:
                        self.ip_dict[(_sub, ips)] += 1

                    if ips not in self.ip_dict:
                        self.ip_dict[ips] = 1
                    else:
                        self.ip_dict[ips] += 1

                    if self.ip_dict[(_sub, ips)] > 3 or self.ip_dict[ips] > 6:
                        continue

                    self.found_count += 1
                    msg = cur_sub_domain.ljust(30) + ips
                    self._print_msg(msg, _found_msg=True)
                    self._print_msg()
                    self.result_lines.append(cur_sub_domain.ljust(30) + '\t' + ips)
                    self.result_domains.append(cur_sub_domain)
                    self.result_ips.extend(ips.split(", "))
                    try:
                        self.resolvers[j].query('lijiejietest.' + cur_sub_domain)
                    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer) as e:
                        self.queue.put((999999999, '{next_sub}.' + sub))
                    except:
                        pass

            except (dns.resolver.NXDOMAIN, dns.name.EmptyLabel) as e:
                pass
            except (dns.resolver.NoNameservers, dns.resolver.NoAnswer, dns.exception.Timeout) as e:
                pass
            except Exception as e:
                import traceback
                traceback.print_exc()
                with open(os.path.join(self.basedir,'ouput','errors.log'), 'a') as errFile:
                    errFile.write('[%s] %s %s\n' % (type(e), cur_sub_domain, e))
            self._print_msg()

    def run(self):
        threads = [gevent.spawn(self._scan, i) for i in range(self.threads)]

        try:
            gevent.joinall(threads)
        except KeyboardInterrupt, e:
            msg = '[WARNING] User aborted.'
            sys.stdout.write('\r' + msg + ' ' * (self.console_width - len(msg)) + '\n\r')
            sys.stdout.flush()


if __name__ == '__main__':
    d = SubNameBrute(target='qpgame.com')
    d.run()
    print d.result_lines
