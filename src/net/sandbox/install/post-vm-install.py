#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

path = os.path.realpath(__file__)
while True:
    path = os.path.dirname(path)
    if os.path.basename(path) == 'src': break
sys.path.append(path)

import grp
import pwd
import subprocess
import urllib2

from net.sandbox.install.util.apt_get import apt_get
from net.sandbox.install.util.conftools import conf_loader
from net.sandbox.install.util.nettools import nettools
from net.sandbox.install.util.patchtools import patchtools
from net.sandbox.install.util.restools import restools

CONF_FILE = restools.get_resource_file('post-install-conf.json')
conf = conf_loader.load_from_file(CONF_FILE)

def install_vbox_additions():
    print "Installation des additions invité..."
    vbox_version = conf.get('vbox-version')
    iso_prefix = conf.get('vbox-additions.iso-prefix')
    additions_mount_point = conf.get('vbox-additions.mount-point')
    url_pattern = conf.get('vbox-additions.url-pattern')
    executable_path = conf.get('vbox-additions.executable-path')
    
    uname = os.uname()[2]
    apt_get.install(['build-essential', 'linux-headers-%s' % uname, 'dkms'])
    additions_iso_file = os.tempnam(iso_prefix)  # TODO remplacer tempnam
    nettools.download(url_pattern % (vbox_version, vbox_version), additions_iso_file)
    os.mkdir(additions_mount_point)
    try:
        subprocess.check_call(['mount', '-o', 'loop', '-t', 'iso9660', additions_iso_file, additions_mount_point])
        try:
            subprocess.call([os.path.join(additions_mount_point, executable_path)])
        finally:
            subprocess.check_call(['umount', additions_mount_point])
    finally:
        os.rmdir(additions_mount_point)
        
def setup_networking():
    print "Configuration réseau..."
    patchtools.apply_patch(restools.get_resource_file('interfaces.patch'), '/etc/network/interfaces')
    patchtools.apply_patch(restools.get_resource_file('hosts.patch'), '/etc/hosts')
    subprocess.check_call(['service', 'networking', 'restart'])

def setup_sandbox_drive():
    print "Configuration des dossiers partagés..."
    umask = conf.get('sandbox-drive.umask')
    mountpoint = conf.get('sandbox-drive.mountpoint')
    symlink_path = conf.get('sandbox-drive.symlink')
    group_name = conf.get('sandbox-drive.group-name')
    owner_name = conf.get('sandbox-drive.owner-name')

    os.mkdir(mountpoint)
    os.symlink(mountpoint, symlink_path)
    subprocess.check_call(['groupadd', group_name])
    subprocess.check_call(['usermod', '-a', '-G', 'vboxsf', owner_name])
    subprocess.check_call(['usermod', '-a', '-G', group_name, owner_name])
    patchtools.apply_patch(restools.get_resource_file('fstab.patch'), '/etc/fstab')
    
    drive_uid = pwd.getpwnam(owner_name).pw_uid
    drive_gid = grp.getgrnam(group_name).gr_gid
    tokens = {
             'mountpoint': mountpoint,
             'umask': umask,
             'gid': str(drive_gid),
             'uid': str(drive_uid)
             }
    patchtools.replace_tokens(tokens, '/etc/fstab')
    subprocess.check_call(['mount', '-a'])
    
def setup_grub():
    print "Configuration grub..."
    patchtools.apply_patch(restools.get_resource_file('grub.patch'), '/etc/default/grub')
    subprocess.check_call(['update-grub'])
    
def setup_swap():
    print "Configuration swapiness..."
    patchtools.apply_patch(restools.get_resource_file('sysctl.conf.patch'), '/etc/sysctl.conf')
    subprocess.check_call(['sysctl', '-w', 'vm.swappiness=10'])

if __name__ == '__main__':
    setup_networking()
    setup_grub()
    setup_swap()
    install_vbox_additions()
    setup_sandbox_drive()
