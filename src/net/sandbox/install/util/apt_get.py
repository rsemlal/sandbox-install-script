#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess


class apt_get(object):

    @classmethod
    def install(cls, packages, force = False):
        pkg_names = packages
        if type(pkg_names).__name__ == 'str':
            pkg_names = [pkg_names]
        command = ['apt-get', 'install', '-y']
        if force:
            command += '-f'
        command += pkg_names
        subprocess.check_call(command)
        
    @classmethod
    def update(cls):
        command = ['apt-get', 'update']
        subprocess.check_call(command)