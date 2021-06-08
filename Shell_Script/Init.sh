#!/bin/bash

cd /home/kimbelly/Run_mitmproxy

dir=/home/mitmproxyuser 

for i in {1..1000}; do
	touch run_mitmproxy_$i.sh

	echo "#!/bin/bash" >> run_mitmproxy_$i.sh
	echo "sudo -u mitmproxyuser -H bash -c '$dir/.local/bin/mitmdump --mode transparent --showhost --set block_global=false -s $dir/mitmproxy/examples/contrib/har_dump.py -w $dir/dump_mitm/dump_$i.mitm --set hardump=$dir/dump_har/dump_$i.har'" >> run_mitmproxy_$i.sh
	
	sudo chmod +x run_mitmproxy_$i.sh
	echo "kimbelly ALL=(ALL) NOPASSWD: /home/kimbelly/Run_mitmproxy/run_mitmproxy_$i.sh" | sudo tee -a /etc/sudoers
done

# Stop mitmproxy
touch stop_mitmproxy.sh

echo "#!/bin/bash" >> stop_mitmproxy.sh
echo "sudo kill -9 \$(sudo lsof -t -i:8080)" >> stop_mitmproxy.sh
	
sudo chmod +x stop_mitmproxy.sh
echo "kimbelly ALL=(ALL) NOPASSWD: /home/kimbelly/Run_mitmproxy/stop_mitmproxy.sh" | sudo tee -a /etc/sudoers
