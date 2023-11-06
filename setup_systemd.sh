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
    Type=oneshot
    ExecStart=$venv_python $(pwd)/src/main.py
    ExecStopPost=/bin/sh -c 'if [ \"\$\$EXIT_STATUS\" = 1 ]; then $venv_python $(pwd)/src/debug.py; fi'
    " > $systemd_service_path
}

if [ "$(id -u)" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi


echo Setting discord bot as systemd service
update_service
update_timer
sudo systemctl daemon-reload
sudo systemctl enable $bot_systemd_name.timer
sudo systemctl start $bot_systemd_name.timer

if [ ! -f src/config.py ]; then
  echo Warning. run setup.py to setup discord secrets
fi