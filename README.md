# PFDTaneTestingScripts

# How to install project

Clone retest branch of this project


(if Desbordante not installed: follow instructions from "Build instrucitons" section from https://github.com/iliya-b/Desbordante/tree/pfdtane-nongeneralized, and clone this repo)

copy .SO file from folder Desbordante/build/target/  to the root of this project  PFDTaneTestingScripts


Create venv:

`python3 -m venv venv`

`source venv/bin/activate`

Install requirements:

`pip install -r requirements.txt`



# How to generate mesuares

Create folder good_datasets

Add datasets to this folder. All datasets should be in csv format

Remove out folder, if present

Run `python3 generate_config.py`

Run `python3 main.py`