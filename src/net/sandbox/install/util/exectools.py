#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
from time import time

from net.sandbox.install.util import logdef

def __log_stream__(log_buffer, prefix, logger=logdef.logger):
    remaining_buffer = log_buffer
    while "\n" in remaining_buffer:
        [line, remaining_buffer] = remaining_buffer.split('\n', 1)
        if logger: logger.debug("%s%s", prefix, line)
    return remaining_buffer
    
def __finalize_log_stream__(log_buffer, prefix, logger=logdef.logger):
    for line in log_buffer.split("\n"): logger.debug("%s%s", prefix, line)
        
def call_command(command, logger=logdef.logger):
    if logger: logger.debug("calling command %s... [", command)
    t0 = time()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    strm = process.stdout
    end_of_file = False
    log_buffer = ""
    try:
        while not end_of_file:
            buff = strm.read(3)
            log_buffer = __log_stream__(log_buffer + buff, "   ", logger=logger)
            end_of_file = len(buff) == 0
    finally:
        strm.close()
        __finalize_log_stream__(log_buffer, "   ", logger)
    retcode = process.wait()
    t = time() - t0
    if logger: logger.debug("] return code was %d, executed in %f seconds", retcode, t)
    return retcode == 0
    
def check_call_command(command, logger=logdef.logger):
    result = call_command(command, logger=logger)
    if not result: raise Exception("Non 0 return code")

if __name__ == '__main__':
    pass