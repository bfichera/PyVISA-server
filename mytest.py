import socket
import sys
import time

import dill as pickle

import instruments.server.messages as messages


def check_output(original_message):
    returned_message = messages.EmptyMessage()
    while isinstance(returned_message, messages.EmptyMessage):
        check_message = messages.RequestReturnMessage(original_message)
        sock.sendall(pickle.dumps(check_message))
        data = sock.recv(1024)
        returned_message = pickle.loads(data)
    return returned_message


HOST = '127.0.0.1'
PORT = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

message1 = messages.NewInstrumentMessage('bk_1686B', 'ASRL/dev/ttyUSB0::INSTR')
sock.sendall(pickle.dumps(message1))
sock.recv(1024)

message4 = messages.RunMethodMessage('bk_1686B', 'init')
sock.sendall(pickle.dumps(message4))
sock.recv(1024)

message5 = messages.RunMethodMessage('bk_1686B', 'query', 'GETS')
sock.sendall(pickle.dumps(message5))
sock.recv(1024)

print(check_output(message5).value)
