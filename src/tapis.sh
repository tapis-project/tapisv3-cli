#!/bin/bash
. "$(dirname $0)/env/bin/activate"
python3 "$(dirname $0)/main.py" "${@}"
deactivate