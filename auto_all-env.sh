#!/bin/sh
set -x

parent_dir="$PWD"
date_time=$(date +"%Y-%m""_%H-%M")
for dir in "$parent_dir/env_files"/*.env; do
    dir_name="${dir%/}"

    set -a
    source "$dir_name"
    set +a


    export ENV_FILE_PATH="$dir_name"
    export BASH_TIME="$date_time"
    echo "Running script for folder: $dir_name"
    python main.py

done 