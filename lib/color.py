# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import colorama

class color:#if not class,when call G\Y\B,the colorama.init() will not be executed. Error will occure!!!
    def __init__(self):
        colorama.init()
        self.G = colorama.Fore.GREEN  # green
        self.Y = colorama.Fore.YELLOW  # yellow
        self.B = colorama.Fore.BLUE # blue
        self.R = colorama.Fore.RED  # red
        self.W = colorama.Fore.WHITE  # white

color = color()