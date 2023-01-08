from socket import *
from mcping.util import to_varint, recv_varint
from struct import pack
from threading import current_thread
import json


def query(host: str, port: int, socket_timeout: int) -> dict:
    with socket(AF_INET, SOCK_STREAM) as s:
        try:
            s.settimeout(socket_timeout)
            s.connect((host, port))
            print(current_thread().name + ": Connected to " + host)

            host = host.encode("utf8")
            host_data = to_varint(len(host)) + host
            port_data = pack("H", port)

            data = b'\x00\x00' + host_data + port_data + b'\x01'
            s.send(to_varint(len(data)) + data)
            data = b'\x00'
            s.send(to_varint(len(data)) + data)
            print(current_thread().name + ": Send success")

            r = b""
            r_length = recv_varint(s)
            r_id = recv_varint(s)
            if r_id > r_length:
                recv_varint(s)

            r_extra_length = recv_varint(s)
            while len(r) < r_extra_length:
                r += s.recv(r_extra_length)
            print(current_thread().name + ": Recv success")
        except Exception:
            print(current_thread().name + ": Query failed")
            s.close()
            return {}
        s.close()
        if r:
            return json.loads(r.decode("utf8"))
        return {}
