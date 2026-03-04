#!/bin/bash

# define file to read
 file="password.txt"

 echo -e "\e[34m[+] start to analyze...\e[0m"

 # order to read the file line by line
 while read line; do
	 #if line is long less than 6 character it will password to "eazy guess"
	 if [ ${#line} -lt 6 ]; then
		 echo -e "\e[31m[!] fine eazy password (too short): $line\e[0m"
	 else
		 echo -e "\e[32m[+] password $line it save\e[0m"
	 fi
	done < "$file"
