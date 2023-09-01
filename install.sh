#!/bin/bash
source config.sh

update_timer()
{
    echo "[Unit]
    Description=Vyk ruokabotti timer
    [Timer]
    OnCalendar=Mon..Fri $exec_time
    [Install]
    WantedBy=timers.target" > $systemd_timer_path
}

update_service()
{
    echo "[Unit]
    Description=Vyk discord roukalista botti
    [Service]
    OnFailure=/usr/bin/python $(pwd)/src/debug.py
    Type=oneshot
    ExecStart=/usr/bin/python $(pwd)/src/main.py
    " > $systemd_service_path
}

if [ "$(id -u)" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

#echo Creating unprivileged user for the bot
#sudo groupadd $bot_group
#sudo useradd -m -G $bot_group $bot_user

echo Generating python requisites
./tools/generate_regs.sh
pip install -r requirements.txt

echo Setting discord bot as systemd service
update_service
update_timer
sudo systemctl daemon-reload
sudo systemctl enable $bot_systemd_name.timer
sudo systemctl start $bot_systemd_name.timer
echo Done