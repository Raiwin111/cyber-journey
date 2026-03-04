#!/bin/bash
if ! command -v nmap &> /dev/null; then
	echo "Error: nmap is not installed!"
	exit 1
fi

FINE_IP=$(nmap -sV -p- 192.168.1.161)
Multiple_num=6


if [ $Multiple_num -eq 6 ]; then
	echo -e "\e[34m This is ip me and what am i stay $FINE_IP ...[0m"
else 
	echo -e "\e[33m no no no this is not = 6 [0m"
fi
