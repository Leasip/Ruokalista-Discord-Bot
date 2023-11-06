#!/bin/bash

bot_user=ruokabot 
bot_group=ruokabot
bot_systemd_name=bot

systemd_timer_path="/etc/systemd/system/$bot_systemd_name.timer"
systemd_service_path="/etc/systemd/system/$bot_systemd_name.service"

# Venv configuraatio
venv_path="$(pwd)/venv"
venv_python="$venv_path/bin/python"
venv_pip="$venv_path/bin/pip"

# Aika jolloin botti lähettää viestin.
# Muodossa Tunti:minuutti
exec_time="9:30"