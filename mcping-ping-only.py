#!/usr/bin/env python3
from mcping import *
from mcping.util import protocol_dict, remove_section_signs
from sys import argv


if len(argv) < 3:
    print("Usage: ./mcping-ping-only.py [host] [port] {timeout}")
    exit(0)

host = argv[1]
port = int(argv[2])

if len(argv) > 3:
    socket_timeout = int(argv[3])
else:
    socket_timeout = 5


d = query(host, port, socket_timeout)
if not d:
    print("Query failed")
    exit(1)
proto = d["version"]["protocol"]
proto_str = str(proto)
if proto > 1000:
  proto_str += " (snapshot)"
elif proto in protocol_dict:
    proto_str += " (" + protocol_dict[proto] + ")"
else:
    proto_str += " (unknown)"

if "enforcesSecureChat" in d:
    secure_chat = d["enforcesSecureChat"]
else:
    secure_chat = None

if "text" in d["description"]:
    desc = d["description"]["text"]
else:
    desc = d["description"]

print("Software:\t\t" + str(d["version"]["name"]))
print("Protocol:\t\t" + proto_str)
print("MOTD:\t\t\t" + remove_section_signs(str(desc)).strip(" "))
print("Players:\t\t" + str(d["players"]["online"]) + " / " + str(d["players"]["max"]))
print("Secure chat:\t" + str(secure_chat))
