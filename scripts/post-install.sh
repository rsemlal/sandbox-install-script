#!/bin/bash

source "$(readlink -f "$(dirname "$0")")/init.sh" $0

script_path="net/sandbox/install/post_vm_install.py"

python "${src_dir}/${script_path}"