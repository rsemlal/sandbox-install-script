#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import logging #@UnusedImport
import logging.handlers

logger = None

def init_logger(script_file):
    log_dir = '/var/log'
    script_name = os.path.basename(script_file)
    log_file = os.path.join(log_dir, '%s.log' % script_name)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    logger = logging.getLogger(script_name)
    handler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    pass