# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import logging
import sys
import os
sys.path.extend("E:\wolaidai\github\Teemo\\")
reload(sys)

LOGGER = logging.getLogger("TeemoLog")

LOGGER_HANDLER = None
try:
    from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler

    disableColor = False

    for argument in sys.argv:
        if "disable-col" in argument:
            disableColor = True
            break

    if disableColor:
        LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
    else:
        LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
except ImportError,e:
    #print e
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(logging.INFO)

logger = LOGGER

if __name__ == "__main__":
    engine_name ="xx"
    logger.warning("warning")
    logger.info("log")
    logger.debug("debug")
    logger.error("sss")
    logger.info("Searching now in {0}..".format(engine_name))
    print os.path.basename(__file__)