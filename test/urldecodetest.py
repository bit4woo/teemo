__author__ = 'bit4'
import urllib

a= "%%25%32%35%25%33%32%25%33%35%25%33%32%25%34%36"

b = urllib.unquote(a)
print b