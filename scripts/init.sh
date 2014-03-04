#!/bin/bash

shell_script=$1
base_dir=$(readlink -f "$(dirname ${shell_script})/..")
scripts_dir="${base_dir}/scripts"
src_dir="${base_dir}/src"
PYTHONPATH="${PYTHONPATH}:${src_dir}"

export PYTHONPATH