#!/bin/bash

gcc checker.c -o checker

echo "---Security system Login ---"
read -sp "Enter Password : " user_pass
echo "" #new line

./checker "$user_pass" | python3 report.py
