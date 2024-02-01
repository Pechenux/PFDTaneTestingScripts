# PFDTaneTestingScripts

# How to install project

Clone https://github.com/iliya-b/Desbordante

Change directory to Desbordante

Switch to "pfdtane-nongeneralized" branch

Build Desbordante (skip creating python venv in instructions)

Go back to the root of this project

Create venv:

`python3 -m venv venv`

`source venv/bin/activate`

Install requirements:

`pip install -r requirements.txt`

Change directory to Desbordante

Run `python3 -m pip install .`

# How to generate mesuares

Create folder good_datasets

Add datasets to this folder. All datasets should be in csv format

Remove out folder, if present

Run `python3 generate_config.py`

Run `python3 main.py`