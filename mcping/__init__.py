from socket import *
from mcping.util import varint
from struct import pack
import json


def query(host: str, port: int, timeout: int) -> list:
    with socket(AF_INET, SOCK_STREAM) as s:
        host = host.encode("utf8")
        host_data = varint(len(host)) + host
        port_data = pack("H", port)

        s.settimeout(timeout)
        s.connect((host, port))
        data = b'\x00\x00' + host_data + port_data + b'\x01'
        s.send(varint(len(data)) + data)
        data = b'\x00'
        s.send(varint(len(data)) + data)
        r = s.recv(2048)

        if not r:
            return []
        print(r)
        return []
