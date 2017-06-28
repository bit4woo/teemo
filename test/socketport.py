import socket

default_proxies = {
    "http": "http://127.0.0.1:9999/",
    "https": "http://127.0.0.1:9999/",
}

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.settimeout(2)
ip = default_proxies['http'].split("/")[-2].split(":")[0]
port = default_proxies['http'].split("/")[-2].split(":")[1]
sk.connect((ip,int(port)))
print sk
sk.close