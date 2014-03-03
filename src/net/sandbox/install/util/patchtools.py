#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
from subprocess import Popen, PIPE

class patchtools(object):
    
    @classmethod
    def create_patch(cls, original_file, modified_file, patch_file):
        with open(patch_file, 'w') as fd:
            subprocess.call(['diff', '-Naur', original_file, modified_file], stdout = fd)
            
    @classmethod
    def apply_patch(cls, patch_file, original_file, destination_file=None):
        if not destination_file:
            destination_file = original_file
        p = Popen(['patch', '-fu', '--input=%s' % patch_file, '--output=-', original_file], stdout=PIPE)
        content, _ = p.communicate()
        assert p.returncode == 0
        with open(destination_file, 'w') as fd:
            fd.write(content)
        
    @classmethod
    def reverse_patch(cls, patch_file, original_file, destination_file=None):
        if not destination_file:
            destination_file = original_file
        p = Popen(['patch', '-Rfu', '--input=%s' % patch_file, '--output=-', original_file], stdout=PIPE)
        content, _ = p.communicate()
        assert p.returncode == 0
        with open(destination_file, 'w') as fd:
            fd.write(content)
        
    @classmethod
    def replace_tokens(cls, tokens, source_file, destination_file = None):
        if not destination_file: destination_file = source_file
        with open(source_file, 'r') as fd: text = fd.read()
        for key in tokens.keys(): text = text.replace('${%s}' % key, tokens[key])
        with open(destination_file, 'w') as fd: fd.write(text)
        
if __name__ == '__main__':
    import os
    import hashlib
    
    f1 = os.tempnam()
    f2 = os.tempnam()
    f3 = os.tempnam()
    f4 = os.tempnam()
    fp = os.tempnam()
    
    print 'f1 = %s' % f1
    print 'f2 = %s' % f2
    print 'f3 = %s' % f3
    print 'f4 = %s' % f4
    
    with open(f1, 'w') as fd1:
        fd1.write('line 1\n')
        fd1.write('line 2\n')
        fd1.write('line 3\n')
    with open(f2, 'w') as fd2:
        fd2.write('line 1\n')
        fd2.write('line 1.5\n')
        
    patchtools.create_patch(f1, f2, fp)
    
    patchtools.apply_patch(fp, f1, f3)
    patchtools.reverse_patch(fp, f3, f4)
    
    h1 = hashlib.md5(open(f1).read()).hexdigest()
    h2 = hashlib.md5(open(f2).read()).hexdigest()
    h3 = hashlib.md5(open(f3).read()).hexdigest()
    h4 = hashlib.md5(open(f4).read()).hexdigest()
    
    assert h2 == h3
    assert h1 == h4
