#!/bin/bash

# Check for TACC credentials. If they don't exist, prompt
# the user to create them.
if ! bash ./auth/configure.sh; then
    exit
fi

# Expose configs
. configs/tacc_credentials

if [[ ! -f "./modules/$1/$2.py" ]]; then
    printf "Invalid module '${1} ${2}'. No file named './modules/$1/$2.py'"
    exit
fi

python3 ./main.py $TACC_USERNAME $TACC_PASSWORD "${@}"

# python3 ./$1/$2.py $TACC_USERNAME $TACC_PASSWORD "${@:3}"

