#!/bin/bash
source config.sh

$venv_pip install pipreqs
source $venv_path; pipreqs --force
