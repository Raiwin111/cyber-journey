#!/bin/bash

#INPUT URL FROM USER
echo -e "\e[32m[+] URL Web for serching (such as http://example.com)\e[0m"
read url

echo -e "\e[31m[+] will pull infomation from $url ... \e[0m"

#Use curl pulling code and use grep find line it has signager 
curl -s "$url" | grep "" > index.html


