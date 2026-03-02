#!/bin/bash
read -p "input ip to scan : " target_ip
echo "[+] about to scan ... please wait for a moment"
#ask ip


#run nmap put in file
echo -e "\e[33m[+] scannig $target_ip ... please wait\e[0m"
nmap -Pn -F "$target_ip" > scan_temp.txt

# Input & Variables
 if [ ! -s scan_temp.txt ]; then
	 echo "[-] nmap not found infomation (maybe it block by firewall )"
 else
	 #sort line only port open
	 scan_rsult=$(grep "open" scan_temp.txt)


# use $() to take result and cut space back = delete it all
scan_result=$(nmap -Pn -F   "$target_ip" | grep "open")

#Final logic check
	if [ -z "$scan_result" ]; then
		echo -e "\e [31m [-] not found port open on $target_ip \e[0m"
		echo "$scan_result"
	else 
		echo -e "\e[32m[+] found port open : \e[0m"
		echo "$scan_result"
	fi
fi
