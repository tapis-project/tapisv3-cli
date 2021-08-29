#!/bin/bash

# Check for TACC credentials. If they don't exist, prompt
# the user to create them.
if ! bash ./auth/configure.sh; then
    exit
fi

# Expose configs
. configs/tacc_credentials

python3 ./main.py $TACC_USERNAME $TACC_PASSWORD "${@}"

