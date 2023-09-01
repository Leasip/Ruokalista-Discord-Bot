#!/bin/bash
bot_user=ruokabot 
bot_group=ruokabot
bot_systemd_name=bot

systemd_timer_path="/etc/systemd/system/$bot_systemd_name.timer"
systemd_service_path="/etc/systemd/system/$bot_systemd_name.service"

# Aika jolloin botti lähettää viestin.
# Muodossa Tunti:minuutti
exec_time="9:30"