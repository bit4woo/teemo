__author__ = 'bit4'
import queue


def callsites_thread(a,q_domains=None):

    for domain in a:
        q_domains.put(domain)
    #return list(set(final_domains))


a=[1,2,3]
device_que=queue.Queue()
callsites_thread(a,device_que)

device=device_que.get()
print device