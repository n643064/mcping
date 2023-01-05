from socket import *
from struct import pack
import json


def varint(data):
    out = b''
    while data != 0:
        byte = data & 0x7F
        data >>= 7
        out += pack('B', byte | (0x80 if data > 0 else 0))
    return out


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
        print(s.recv(1024))


