#!/usr/bin/python
# -*- coding: utf-8 -*-
import grp
import os
import pwd

from net.sandbox.install.util import patchtools, aptgettools, filetools, exectools,\
    conftools
from net.sandbox.install.util.consoletools import console
from net.sandbox.install.util.nettools import nettools
from net.sandbox.install.util.restools import restools


CONF_FILE = restools.get_resource_file('post-install-conf.json')
conf = conftools.load_from_file(CONF_FILE)

def install_vbox_additions():
    vbox_version = conf.get('vbox-version')
    iso_prefix = conf.get('vbox-additions.iso-prefix')
    additions_mount_point = conf.get('vbox-additions.mount-point')
    url_pattern = conf.get('vbox-additions.url-pattern')
    executable_path = conf.get('vbox-additions.executable-path')
    
    uname = os.uname()[2]
    aptgettools.install(['build-essential', 'linux-headers-%s' % uname, 'dkms'])
    additions_iso_file = filetools.temp_file(iso_prefix, '.iso')
    nettools.download(url_pattern % (vbox_version, vbox_version), additions_iso_file)
    os.mkdir(additions_mount_point)
    try:
        exectools.check_call_command(['mount', '-o', 'loop', '-t', 'iso9660', additions_iso_file, additions_mount_point])
        try:
            exectools.call_command([os.path.join(additions_mount_point, executable_path)])
        finally:
            exectools.check_call_command(['umount', additions_mount_point])
    finally: os.rmdir(additions_mount_point)
        
def setup_networking():
    patchtools.apply_patch(restools.get_resource_file('interfaces.patch'), '/etc/network/interfaces')
    patchtools.apply_patch(restools.get_resource_file('hosts.patch'), '/etc/hosts')
    exectools.check_call_command(['service', 'networking', 'restart'])

def setup_sandbox_drive():
    umask = conf.get('sandbox-drive.umask')
    mountpoint = conf.get('sandbox-drive.mountpoint')
    symlink_path = conf.get('sandbox-drive.symlink')
    group_name = conf.get('sandbox-drive.group-name')
    owner_name = conf.get('sandbox-drive.owner-name')

    os.mkdir(mountpoint)
    os.symlink(mountpoint, symlink_path)
    exectools.check_call_command(['groupadd', group_name])
    exectools.check_call_command(['usermod', '-a', '-G', 'vboxsf', owner_name])
    exectools.check_call_command(['usermod', '-a', '-G', group_name, owner_name])
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
    exectools.check_call_command(['mount', '-a'])
    
def setup_grub():
    patchtools.apply_patch(restools.get_resource_file('grub.patch'), '/etc/default/grub')
    exectools.check_call_command(['update-grub'])
    
def setup_swap():
    patchtools.apply_patch(restools.get_resource_file('sysctl.conf.patch'), '/etc/sysctl.conf')
    exectools.check_call_command(['sysctl', '-w', 'vm.swappiness=10'])

if __name__ == '__main__':
    import sys
    from net.sandbox.install.util import logdef
    
    logdef.init_logger(sys.argv[0])
    console = console()
    
    try:
        print "Configuration réseau..."
        setup_networking()
        
        print "Configuration grub..."
        setup_grub()
        
        print "Configuration swapiness..."
        setup_swap()
        
        print "Installation des additions invité..."
        install_vbox_additions()
        
        print "Configuration des dossiers partagés..."
        setup_sandbox_drive()
    except Exception as e:
        console.writeln("Erreur")