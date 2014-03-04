#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import tempfile
import random
import hashlib

def temp_file(prefix="~", suffix=".tmp"):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    tmpdir = tempfile.gettempdir()
    while True:
        rchars = "".join(random.sample(chars, 6))
        path = os.path.join(tmpdir, '%s%s%s' % (prefix, rchars, suffix))
        if not os.path.exists(path): break
    return path

def md5(path):
    return hashlib.md5(open(path).read()).hexdigest()

if __name__ == '__main__':
    print temp_file("tmp-", ".txt")
