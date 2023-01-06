#!/usr/bin/env python3
from mcping.dnsd import *
from sys import argv, stderr
if len(argv) < 2:
    stderr.write("Usage: ./subdomain-finder.py [domain]\n")
    exit(0)

d = query_domain(argv[1])

if not d:
    stderr.write("Query failed\n")
    exit(0)

for s in d:
    print(s)