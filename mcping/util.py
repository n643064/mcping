import struct
from socket import socket
import re

SEGMENT = 0x7F
CONTINUE = 0x80

def to_varint(data) -> bytes:
    out: bytes = b''
    while data != 0:
        byte = data & SEGMENT
        data >>= 7
        out += struct.pack('B', byte | (CONTINUE if data > 0 else 0))
    return out

def recv_varint(s: socket) -> int:
    data = 0
    for i in range(5):
        r = s.recv(1)
        if (len(r)) == 0:
            break
        b = ord(r)
        data |= (b & SEGMENT) << 7 * i
        if not b & CONTINUE:
            break
    return data


def remove_section_signs(s: str) -> str:
    s2 = ""
    i = 0
    while i < len(s):
        if s[i] == "§":
            i += 1
        else:
            s2 += s[i]
        i += 1
    return s2


class Info:
    def __init__(self, host: str, software: str, proto: int, motd: str, max_players: int, current_players: int, secure_chat: bool):
        self.host = host
        self.software = software
        self.proto = proto
        self.motd = motd
        self.max_players = max_players
        self.current_players = current_players
        self.secure_chat = secure_chat

    @classmethod
    def from_dict(cls, host: str, d: dict):
        if "version" in d:
            software = d["version"]["name"]
            proto = d["version"]["protocol"]
        else:
            software = ""
            proto = 1337
        if "enforcesSecureChat" in d:
            secure_chat = d["enforcesSecureChat"]
        else:
            secure_chat = None

        if "description" in d:
            if "text" in d["description"]:
                motd = d["description"]["text"]
            else:
                motd = d["description"]
        else:
            motd = "<not received>"
        if "players" in d:
            p_current = d["players"]["online"]
            p_max = d["players"]["max"]
        else:
            p_max = 0
            p_current = 0
        return Info(host, software, proto, motd, p_max, p_current, secure_chat)

    def sanitize(self):
        pattern = r"drop|delete|exec"
        self.software = re.sub(pattern, "", self.software, flags=re.IGNORECASE)
        self.motd = re.sub(pattern, "", self.motd, flags=re.IGNORECASE)


protocol_dict = {
    761: "1.19.3",
    760: "1.19.1-2",
    759: "1.19",
    758: "1.18.2",
    756: "1.17.1",
    755: "1.17",
    754: "1.16.4-5",
    753: "1.16.3",
    751: "1.16.2",
    736: "1.16.1",
    735: "1.16",
    47: "1.8.*"
}
# TODO: Add more protocol versions
