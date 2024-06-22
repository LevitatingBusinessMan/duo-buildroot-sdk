#!/bin/sh

# Put the program you want to run automatically here

sleep 3
echo Starting wpa_supplicant
wpa_supplicant -B -P /var/run/wpa_supplicant.pid -i wlan0 -c /etc/wpa_supplicant.conf -f /var/log/wpa_supplicant.log
echo Starting rtl_tcp
rtl_tcp -a 0.0.0.0 -D 2> /var/log/rtl_tcp.log >/dev/null &
echo $! > /var/run/rtl_tcp.pid
