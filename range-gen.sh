#!/bin/sh

if [ $# -ne 2 ]
then
    echo "Usage: ./range-gen [prefix] [range]"
    exit
fi

for i in `seq 1 $2`
do
  echo "$1$i"
done