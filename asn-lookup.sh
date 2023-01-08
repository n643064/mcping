#!/bin/sh

if [ $# -ne 1 ]
then
  echo "Usage: ./asn-lookup.sh [ip]"
  exit
fi
ASN=$(whois -h whois.radb.net $1 | grep '^origin' | tail -n 1 | awk -F" " '{print($2)}')

whois -h whois.radb.net "!g$ASN" | grep -Eo "([0-9.]+){4}/[0-9]+" | cut -d"/" -f1
