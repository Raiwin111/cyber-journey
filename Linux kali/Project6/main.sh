#!/bin/bash

echo "== Password Security Scanner =="

read -p "Enter password to scan: " PASS

echo "Analyzing ..."

SCORE=$(python3 check_pass.py "$PASS")

echo "Result from Python : $SCORE"
if [ "$SCORE" == "Strong (Good job!)" ]; then
	echo "Access Granted!"
else
	echo "Please update your password."
fi
