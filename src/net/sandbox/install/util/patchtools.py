#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess


def create_patch(original_file, modified_file, patch_file):
    with open(patch_file, 'w') as fd:
        subprocess.call(['diff', '-Naur', original_file, modified_file], stdout = fd, stderr = subprocess.PIPE)
        
def apply_patch(patch_file, original_file, destination_file=None):
    if not destination_file:
        destination_file = original_file
    p = subprocess.Popen(['patch', '-fu', '--input=%s' % patch_file, '--output=-', original_file], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    content, _ = p.communicate()
    assert p.returncode == 0
    with open(destination_file, 'w') as fd:
        fd.write(content)

def reverse_patch(patch_file, original_file, destination_file=None):
    if not destination_file:
        destination_file = original_file
    p = subprocess.Popen(['patch', '-Rfu', '--input=%s' % patch_file, '--output=-', original_file], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    content, _ = p.communicate()
    assert p.returncode == 0
    with open(destination_file, 'w') as fd:
        fd.write(content)

def replace_tokens(tokens, source_file, destination_file = None):
    if not destination_file: destination_file = source_file
    with open(source_file, 'r') as fd: text = fd.read()
    for key in tokens.keys(): text = text.replace('${%s}' % key, tokens[key])
    with open(destination_file, 'w') as fd: fd.write(text)
        
if __name__ == '__main__':
    from net.sandbox.install.util import filetools
    
    original_file = filetools.temp_file()
    modified_file = filetools.temp_file()
    patched_file = filetools.temp_file()
    reversed_patch_file = filetools.temp_file()
    patch_file = filetools.temp_file()
    
    with open(original_file, 'w') as fd1:
        fd1.write('line 1\n')
        fd1.write('line 2\n')
        fd1.write('line 3\n')
    with open(modified_file, 'w') as fd2:
        fd2.write('line 1\n')
        fd2.write('line 1.5\n')
        
    create_patch(original_file, modified_file, patch_file)
    
    apply_patch(patch_file, original_file, patched_file)
    reverse_patch(patch_file, patched_file, reversed_patch_file)
    
    h1 = filetools.md5(original_file)
    h2 = filetools.md5(modified_file)
    h3 = filetools.md5(patched_file)
    h4 = filetools.md5(reversed_patch_file)
    
    assert h2 == h3
    assert h1 == h4
