#!/bin/sh

parent_dir="$(dirname "$0")"
for dir in "$parent_dir/env_files"/*; do
    dir_name="${dir%/}"
    echo "Running script for folder: $dir"
    export dir_name
    python main.py --input "$dir_name"
done