#!/bin/bash
date=$(date +"%m-%d-%Y")
now=$(date +"%r")
filename="/home/zarbalatrax/logs/log-$date"
echo -e "\n\n----BOOT----\nTime: $now\n\n" >> $filename
nohup python -u /home/zarbalatrax/main/main.py 2>&1 | tee -a $filename &
jobs
disown -h %1
jobs