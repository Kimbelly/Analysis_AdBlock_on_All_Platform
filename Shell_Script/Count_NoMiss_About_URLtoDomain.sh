#!/bin/bash

# Use '$ bash xxx.sh', don't use '$ sh xxx.sh'
ReadMe="/home/kimbelly/Analysis/Block_Ads/AndroidVersion/Block_Ads_Uniq_1/ReadMe_1"
ReadMe_Miss="/home/kimbelly/Analysis/URL_vs_Domain/AndroidVersion/Miss_URLtoDomain_Uniq_1/ReadMe_Miss_1"

declare -a domain_arr=("Domain_AdGuard_DNS_Filter" "Domain_StevenBlack" "Domain_AdAway"
						"Domain_Someonewhocares" "Domain_Peter_Lowe_List" "Domain_EasylistChina+Easylist"
						"Domain_Combine_All")

declare -a url_arr=("URL_EasylistChina+Easylist" "URL_AdGuard_Base_Filter_Optimized" 
					"URL_Easylists" "URL_Combine_All")

sum=0
i=0
total=1 # please check the number

for url_ele in ${url_arr[@]}; do
	echo "==============${url_ele}=============="
	grep "${url_ele}" $ReadMe | while read -r line ; do
		NUM=$(echo "$line" | grep -o '#[0-9]*' | tr -dc '0-9')
		((sum+=NUM))
		((i+=1))
	
		if [ "$i" = "$total" ]
		then
			echo $sum
			for domain_ele in ${domain_arr[@]}; do
				no_miss_sum=0
				j=0
			
				grep -h -A 8 "${url_ele}" $ReadMe_Miss | grep "${domain_ele}" | \
				while read -r line ; do
					num=$(echo "$line" | grep -o '#[0-9]*' | tr -dc '0-9')
					((no_miss_sum+=num))
					((j+=1))
					if [ "$j" = "$total" ]
					then
						echo "${domain_ele}:"
						#awk "BEGIN {printf \"%-8d %-4.1f\n\", ${no_miss_sum}, ${no_miss_sum}/${sum}*100}"
						awk "BEGIN {printf \"%d (%.1f%%)\n\", ${no_miss_sum}, ${no_miss_sum}/${sum}*100}"
					fi
				done
			done
		fi
	done
done

