# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

# Courtesy http://plumberjack.blogspot.com/2010/12/colorizing-logging-output-in-terminals.html
# Tweaked to use colorama for the coloring

import colorama
import logging
import sys

colorama.init()
G = colorama.Fore.GREEN  # green
Y = colorama.Fore.YELLOW  # yellow
B = colorama.Fore.BLUE # blue
R = colorama.Fore.RED  # red
W = colorama.Fore.WHITE  # white

class ColorizingStreamHandler(logging.StreamHandler):
    color_map = {
        logging.DEBUG: colorama.Fore.BLUE,
        logging.INFO: colorama.Fore.GREEN,
        logging.WARNING: colorama.Fore.YELLOW,
        logging.ERROR: colorama.Fore.RED,
        logging.CRITICAL: colorama.Back.RED,
    }

    def __init__(self, stream, color_map=None):
        logging.StreamHandler.__init__(self,
                                       colorama.AnsiToWin32(stream).stream)
        if color_map is not None:
            self.color_map = color_map

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()

    def format(self, record):
        message = logging.StreamHandler.format(self, record)
        if self.is_tty:
            # Don't colorize a traceback
            parts = message.split('\n', 1)
            parts[0] = self.colorize(parts[0], record)
            message = '\n'.join(parts)
        return message

    def colorize(self, message, record):
        try:
            return (self.color_map[record.levelno] + message +
                    colorama.Style.RESET_ALL)
        except KeyError:
            return message


logger = logging.getLogger('Teemo')

LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
LOGGER_HANDLER.setFormatter(FORMATTER)

logger.addHandler(LOGGER_HANDLER)
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    handler = ColorizingStreamHandler(sys.stdout)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')