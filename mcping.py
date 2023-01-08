#!/usr/bin/env python3
from sys import argv, stdin
from threading import *
from mcping import query
from mcping.db import *
from mcping.util import Info

flags = {
    "d": "mcping.db",
    "t": "4",
    "m": "2",
}

help_msg = """Usage: ./mcping [flags]
\t-h\tPrint this message
\t-d\tSpecify database file (mcping.db)
\t-s\tEnable string sanitization
\t-t\tNumber of threads (4)
\t-m\tSocket timeout (2)"""

if "-h" in argv:
    print(help_msg)
    exit(0)

if "-s" in argv:
    sanitize_strings = True
else:
    sanitize_strings = False

for i in range(1, len(argv)):
    if argv[i][0] == '-':
        flags[argv[i][1]] = argv[i + 1]

thread_count = int(flags["t"]) + 1
timeout = int(flags["m"])
conn = connect(flags["d"])
db = conn.cursor()

collected = []
threads = []
def main():
    if not check_table(db, "Servers"):
        create(db)

    for line in stdin:
        while collected:
            insert(db, collected.pop())
            conn.commit()
            print("Committed to db")

        while active_count() == thread_count:
            pass
        l = line.split(" ")
        if not l: continue
        if len(l) == 1:
            port = 25565
        else:
            port = int(l[1])
        s = l[0].strip()
        t = Thread(target=run_target, args=(s, port, timeout), name=s)
        t.start()
        threads.append(t)
    while active_count() != 1:
        pass
    while collected:
        insert(db, collected.pop())
        conn.commit()
        print("Committed to db")


def run_target(host, port, m):
    d = query(host, port, m)
    if d:
        info = Info.from_dict(host, d)
        if info.proto <= 0 or info.max_players == 0:
            return
        if sanitize_strings: info.sanitize()
        collected.append(info)
        print(current_thread().name + ": Collected info for " + host)

if __name__ == "__main__":
    main()
