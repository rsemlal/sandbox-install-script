#!/usr/bin/python
# -*- coding: utf-8 -*-
import json


def load_from_file(filename):
    with open(filename, mode='r') as fd:
        conf = json.load(fd)
        return conf_loader(conf)

class conf_loader(object):
    
    def __init__(self, parsed_config):
        self.__parsed_config = parsed_config
        
    def get(self, key):
        key_path = key.split('.')
        value = self.__parsed_config
        for k in key_path:
            value = value[k]
        return value
        
if __name__ == '__main__':
    from net.sandbox.install.util.restools import restools
    f = restools.get_resource_file('post-install-conf.json')
    print "vbox-version: %s" % conf_loader.load_from_file(f).get("vbox-version")
    print "sandbox-drive.owner-name: %s" % conf_loader.load_from_file(f).get("sandbox-drive.owner-name")