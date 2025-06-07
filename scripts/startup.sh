#!/bin/bash
date=$(date +"%m-%d-%Y")
now=$(date +"%r")
echo -e "\n\n----BOOT----\nTime: $now\n\n"
python -u /home/zarbalatrax/main/main.py
