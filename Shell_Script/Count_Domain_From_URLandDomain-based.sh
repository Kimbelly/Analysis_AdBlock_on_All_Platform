#!/bin/bash

cd /home/kimbelly/Analysis/Count_Domain_From_URLandDomain-based/AndroidVersion/Uniq\(HAR\)_1/

tmp="_compres"
for f1 in ./*
do
	if [ -f "$f1" ]; then
		sort $f1 | uniq -c | sort -g -r -o ./Compress/$f1$tmp
	fi
done

echo "Finished !"
