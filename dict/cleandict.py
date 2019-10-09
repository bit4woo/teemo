# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

listdicts = open("subnames_from_layer.txt","r").readlines()

setdicts = set(listdicts)

fp = open("subnames_from_layer_clean.txt", "w")
for item in setdicts:
    fp.write(item)
fp.close()