import sys

#get value Standard Input (from c)
result = sys.stdin.read().strip()

if result == "SUCCESS":
    print(" [Python] Access Granted: Welcome , Admin")
else:
    print(" [Python] Access Granted: Intrusions detected.")
