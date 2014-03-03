#!/usr/bin/python
# -*- coding: utf-8 -*-
import os


class restools(object):
    RES_DIR_NAME = 'res'
    
    @classmethod
    def get_resource_dir(cls):
        path = os.path.realpath(__file__)
        while True:
            path = os.path.dirname(path)
            res_path = os.path.join(path, cls.RES_DIR_NAME)
            if os.path.isdir(res_path): break
        return res_path
    
    @classmethod
    def get_resource_file(cls, path):
        resource_dir = cls.get_resource_dir()
        full_path = os.path.join(resource_dir, path)
        if os.path.exists(full_path): return full_path
        else: return None

if __name__ == '__main__':
    print restools.get_resource_file('ldap.sandbox.net.init.ldif')