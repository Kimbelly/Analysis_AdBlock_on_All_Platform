#!/bin/bash

dir=/home/mitmproxyuser

# For Ad-Block
#for i in {1..1000}; do
#	sudo -u mitmproxyuser -H bash -c "$dir/.local/bin/mitmdump -n -r $dir/dump_mitm/AdBlock/dump_$i.mitm -s $dir/mitmproxy/examples/contrib/har_dump.py --set hardump=$dir/dump_har/AdBlock/dump_$i.har"
#done

# For No VPN
#for i in {1..1000}; do
#	sudo -u mitmproxyuser -H bash -c "$dir/.local/bin/mitmdump -n -r $dir/dump_mitm/No_VPN/dump_$i.mitm -s $dir/mitmproxy/examples/contrib/har_dump.py --set hardump=$dir/dump_har/No_VPN/dump_$i.har"
#done

# For Ad-Block & DoH Block
#for i in {1..1000}; do
#	sudo -u mitmproxyuser -H bash -c "$dir/.local/bin/mitmdump -n -r $dir/dump_mitm/AdandDoH_Block/dump_$i.mitm -s $dir/mitmproxy/examples/contrib/har_dump.py --set hardump=$dir/dump_har/AdandDoH_Block/dump_$i.har"
#done

# For Only VPN
for i in {1..1000}; do
	sudo -u mitmproxyuser -H bash -c "$dir/.local/bin/mitmdump -n -r $dir/dump_mitm/VPN/dump_$i.mitm -s $dir/mitmproxy/examples/contrib/har_dump.py --set hardump=$dir/dump_har/VPN/dump_$i.har"
done
