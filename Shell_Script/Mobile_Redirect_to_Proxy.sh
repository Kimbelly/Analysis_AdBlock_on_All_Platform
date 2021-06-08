#!/bin/bash

# First, maybe you need to flush all firewall rules
sudo iptables -F
sudo ip6tables -F

sudo iptables -t nat -F
sudo ip6tables -t nat -F

# emulator to mitmproxy
sudo iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner mitmproxyuser --dport 80 -j REDIRECT --to-port 8080
sudo iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner mitmproxyuser --dport 443 -j REDIRECT --to-port 8080
sudo ip6tables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner mitmproxyuser --dport 80 -j REDIRECT --to-port 8080
sudo ip6tables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner mitmproxyuser --dport 443 -j REDIRECT --to-port 8080


# Allow mobile device's http/s traffic redirect to mitm proxy
# so mitm proxy can see traffic and then redirect traffic to ethernet card eno1

#sudo iptables --table nat --append POSTROUTING --out-interface eno1 -j MASQUERADE
# sudo iptables --append FORWARD --in-interface wlxd45d6491bfca -j ACCEPT   ==> no need

#sudo iptables -t nat -A PREROUTING -i wlxd45d6491bfca -p tcp --dport 80 -j REDIRECT --to-port 8081
#sudo iptables -t nat -A PREROUTING -i wlxd45d6491bfca -p tcp --dport 443 -j REDIRECT --to-port 8081
#sudo ip6tables -t nat -A PREROUTING -i wlxd45d6491bfca -p tcp --dport 80 -j REDIRECT --to-port 8081
#sudo ip6tables -t nat -A PREROUTING -i wlxd45d6491bfca -p tcp --dport 443 -j REDIRECT --to-port 8081

# Now, you can let mobile device connect to AP server

# check iptables
#sudo iptables --list -v
#echo "\n================ iptables -L -n -v -t nat ================\n"
#sudo iptables -L -n -v -t nat
#echo "\n================ ip6tables -L -n -v -t nat ================\n"
#sudo ip6tables -L -n  -v -t nat

### Note  ###
# Android VPN => AP => local Proxy (AP and proxy on the same machine)
# sudo iptables -t nat -A PREROUTING -i wlxd45d6491bfca -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 8081
# sudo iptables -t nat -A PREROUTING -i wlxd45d6491bfca -p tcp -m tcp --dport 443 -j REDIRECT --to-ports 8081
# sudo iptables -t nat -A POSTROUTING -o eno1 -j MASQUERADE

