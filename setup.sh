#!/bin/bash
source config.sh

echo Creating a venv
mkdir venv
python -m venv $venv_path

echo Generating python requisites
chmod u+x ./tools/generate_regs.sh
./tools/generate_regs.sh

$venv_pip install -r requirements.txt

# Run secrets setup if config.py doesn't exist
if [ -f config.py ]; then
    $venv_python src/setup.py
fi

# then setup systemd timer
sudo bash setup_systemd.sh