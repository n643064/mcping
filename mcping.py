#!/usr/bin/env python3
from sys import argv, stdin, stdout, stderr
from sqlite3 import connect
from mcping.db import *
from mcping import query
from mcping.db import check_table
from mcping.util import Info

if len(argv) < 3:
    stderr.write("Usage: ./mcping-db [database] [sanitize]\n")
    exit(0)

if argv[2].lower() in ["true", "yes", "on", "1"]:
    schizo_mode = True
else:
    schizo_mode = False

conn = connect(argv[1])
db = conn.cursor()
if not check_table(db, "Servers"):
    create(db)

for line in stdin:
    line = line[:-1]
    if line:
        lines = line.split(" ")
        host = lines[0]
        port = 25565
        timeout = 3
        l = len(lines)
        if l > 1:
            port = int(lines[1])
        if l > 2:
            timeout = int(lines[2])
        d = query(host, port, timeout)\

        if d:
            info = Info.from_dict(host, d)
            if info.proto < 0 or info.max_players == 0:
                continue
            if schizo_mode: info.sanitize()
            insert(db, info)
            conn.commit()
            print("Server inserted into db")


