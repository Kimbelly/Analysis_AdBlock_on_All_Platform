#!/bin/bash

# Use '$ bash xxx.sh', don't use '$ sh xxx.sh'
ReadMe="/home/kimbelly/Analysis/Block_Ads/AndroidVersion/Block_Ads_Uniq_1/ReadMe_1"

sum=0
i=0
total=1 # please check the number
total_request_uniq=1430960 # please check the number

declare -a arr=("Domain_AdGuard_DNS_Filter" "Domain_StevenBlack" "Domain_AdAway"
				"Domain_Someonewhocares" "Domain_Peter_Lowe_List" "Domain_EasylistChina+Easylist"
				"Domain_Combine_All" "URL_EasylistChina+Easylist" "URL_AdGuard_Base_Filter_Optimized" 
				"URL_Easylists" "URL_Combine_All")

for ele in ${arr[@]}; do
	echo "${ele}:"
	grep "${ele}" $ReadMe | while read -r line ; do
		NUM=$(echo "$line" | grep -o '#[0-9]*' | tr -dc '0-9')
		((sum+=NUM))
		((i+=1))
	
		if [ "$i" = "$total" ]
		then
			#awk "BEGIN {printf \"%-8d %-4.1f\n\", ${sum}, ${sum}/${total_request}*100}"
			awk "BEGIN {printf \"%d (%.1f%%)\n\", ${sum}, ${sum}/${total_request_uniq}*100}"
		fi
	done
done
