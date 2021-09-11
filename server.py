import socket
import pickle
import sys

import pyvisa

from info import A, Message
from instruments.bk_1686B import bk_1686B


HOST = '127.0.0.1'
PORT = int(sys.argv[1])

mya = A(3)
myb = A(10)

instruments = {'a':mya, 'b':myb}

known_resource_pyclasses = {'bk_1686B':bk_1686B}

rm = pyvisa.ResourceManager()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = pickle.loads(data)
            if message.instrument_name not in instruments.keys():
                instruments[message.instrument_name] = rm.open_resource(
                    message.name,
                    resource_pyclass=known_resource_pyclasses[
                        message.instrument_name,
                    ],
                )
            out = pickle.dumps(
                getattr(
                    instruments[message.instrument_name],
                    message.name,
                ),
            )
            conn.sendall(out)
