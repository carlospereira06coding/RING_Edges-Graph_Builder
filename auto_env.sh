#!/bin/sh

set -e
set -x

parent_dir="$PWD"
date_time=$(date +"%Y-%m-%d_%H-%M_%Z")
dir_name="$parent_dir/env_files/TTK_Human_WT-aa363.env"


set -a
source "$dir_name"
set +a


export ENV_FILE_PATH="$dir_name"
export BASH_TIME="$date_time"
echo "Running script for .env file: $dir_name"
python main.py

