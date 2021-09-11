import socket
import argparse
import random

import pyvisa
import dill as pickle

from instruments.server.instrumentmanager import MessageHandler


def _getcfg():
    parser = argparse.ArgumentParser(description='Start instruments server')
    parser.add_argument(
        'address',
        dest='address',
        default='127.0.0.1',
    )
    parser.add_argument(
        'port',
        dest='port',
        default=2264,
    )
    args = parser.parse_args
    return args.valuesdict()


def main(cfg):

    host = cfg['address']
    port = cfg['port']

    message_handler = MessageHandler()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    conn, addr = sock.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = pickle.loads(data)
            if message == 'RETURN':
                conn.sendall(
                    pickle.dumps(
                        message_handler.pop(),
                    ),
                )
            else:
                message_handler.process_message(message)


if __name__ == '__main__':
    
    cfg = _getcfg()
    main(cfg)
