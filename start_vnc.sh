#!/bin/bash

# Start VNC server with XFCE
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS

exec startxfce4 &
[vncserver]
command=vncserver
args=:1 -geometry 1920x1080 -depth 24 -localhost