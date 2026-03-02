#!/bin/bash

echo -e "\e[36m[+] Recon Bot Starting ... \e[0m"
read -p "Enter Target URL (e.g., http://example.com):" url

#ST1 Check Server Handle
echo -e "\e [33m[!] Checking Server Header ...\e[0m"
#Use Curl -I pull only Header to look.
server_info=$(curl -I -s "$url" | grep -i "Server")
echo "Result: $server_info"

#ST2 Logic Check (Use if)
if [ -z "$server_info" ]; then
	echo -e "\e[31m[-] Could not get server info. \e[0m"

else echo -e "\e[32m[+] Server detected!\e[0m"
fi

# ST3 Sercret Hunter
echo -e "\e[33m[!] Seraching for sensitive comments...\e [0m"
#sort find only in comment
curl -s "$url" | grep -iE "admin|pass|config|root" > potential_leadks.txt
echo "[+] Done! Check 'potential_leaks.txt' for result."
