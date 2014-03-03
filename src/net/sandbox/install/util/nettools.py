#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import time
import urllib2


class nettools(object):
    BLOCK_SIZE = 8192
    TICK_INTERVAL = 1
    
    KILO_BYTE = 1024
    MEGA_BYTE = KILO_BYTE * KILO_BYTE
    GIGA_BYTE = MEGA_BYTE * KILO_BYTE
    
    @classmethod
    def nice_size(cls, oct_size):
        size = float(oct_size)
        if oct_size <= cls.KILO_BYTE:
            size = size
            unit = 'B'
        elif oct_size <= cls.MEGA_BYTE:
            size = size / cls.KILO_BYTE
            unit = 'KB'
        elif oct_size <= cls.GIGA_BYTE:
            size = size / cls.MEGA_BYTE
            unit = 'MB'
            
        return "%.2f %s" % (size, unit)

    @classmethod
    def download(cls, additions_iso_url, additions_iso_file):
        conn = urllib2.urlopen(additions_iso_url)
        fd = open(additions_iso_file, 'wb')
        file_size = int(conn.info().getheaders("Content-Length")[0])
        print "downloading %s (total size: %s)..." % (additions_iso_url, cls.nice_size(file_size))
        
        last_tick = 0
        p = 0
        while True:
            buff = conn.read(cls.BLOCK_SIZE)
            if not buff:
                break
            
            p += len(buff)
            fd.write(buff)
            tick = time()
            if ((tick - last_tick) >= cls.TICK_INTERVAL) or (p == file_size):
                last_tick = tick
                percent = (100 * p) / file_size
                print "  downloaded %s over %s (%d%%)" % (cls.nice_size(p), cls.nice_size(file_size), percent)

        fd.close()
        print "download completed successfully, output to file: %s" % additions_iso_file
        
if __name__ == '__main__':
    nettools.download("http://download.virtualbox.org/virtualbox/4.3.6/VBoxGuestAdditions_4.3.6.iso", "test.iso")
        