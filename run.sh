#!/usr/bin/bash

source venv/bin/activate &&
rm -rf out &&
python3 generate_config.py &&
python3 main.py