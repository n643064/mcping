#!/bin/sh

if [ $# -ne 1 ]
then
  echo "Usage: ./asn-lookup.sh [domain]"
  exit
fi
IP=$(dig "$1" | grep "$1" | tail -n 1 | awk -F" " '{print($5)}')
ASN=$(whois -h whois.radb.net "$IP" | grep '^origin' | tail -n 1 | awk -F" " '{print($2)}')
whois -h whois.radb.net "!g$ASN" | grep -Eo "([0-9.]+){4}/[0-9]+"
