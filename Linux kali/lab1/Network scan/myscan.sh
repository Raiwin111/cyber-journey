#!/bin/bash

echo "===================================="
echo " 	MY FIRST NET WORK SCANNER	"
echo "===================================="

# input IP from user (this is create varible)
echo -n "show IP for scan: "
read target_ip

# start scan and show text status
echo "scan $target_ip ... please wait a moment"

#Use nmap scan and  send result (Pipe) go to save in file.
#We going to use -F for speed (scan 100 port popular)
nmap -sT -Pn  $target_ip > scan_result.txt

echo "===================================="
echo "scan finish"
echo "result is save in file : scan_result.txt now"
echo "===================================="

# result first 5 line head for example
head -n 10 scan_result.txt
