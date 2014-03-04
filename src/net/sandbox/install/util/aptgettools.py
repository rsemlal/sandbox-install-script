#!/usr/bin/python
# -*- coding: utf-8 -*-
from net.sandbox.install.util import exectools

def install(packages, force = False):
    pkg_names = packages
    if type(pkg_names).__name__ == 'str':
        pkg_names = [pkg_names]
    command = ['apt-get', 'install', '-y']
    if force:
        command += '-f'
    command += pkg_names
    exectools.check_call_command(command)
        
def update():
    exectools.check_call_command(['apt-get', 'update'])