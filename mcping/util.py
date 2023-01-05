import struct

SEGMENT = 0x7F
CONTINUE = 0x80


def varint(data):
    out = b''
    while data != 0:
        byte = data & SEGMENT
        data >>= 7
        out += struct.pack('B', byte | (CONTINUE if data > 0 else 0))
    return out
