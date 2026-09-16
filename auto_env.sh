#!/bin/sh

parent_dir="$(dirname "$0")"
dir_name="$parent_dir/env_files/TTK_Human_WT-aa12.env"
echo "Running script for folder: $dir"
export dir_name
python main.py --input "$dir_name"

