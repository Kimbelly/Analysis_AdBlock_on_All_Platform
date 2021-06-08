#!/bin/bash

# Run AP server
sudo ifconfig wlxd45d6491bfca up 10.20.30.1 netmask 255.255.255.0
sudo service dnsmasq start
sudo hostapd /etc/hostapd/hostapd.conf

# Now, you can let mobile device connect to AP server

