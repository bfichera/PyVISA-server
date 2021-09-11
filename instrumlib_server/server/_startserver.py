import threading
import socket

from .instrumentmanager import _MessageHandler
from . import _messages


class ClientThread(threading.Thread):
    
    def __init__(self, sock, address, message_handler):
        threading.Thread.__init__(self)
        self.sock = sock
        self.address = address
        self.message_handler = message_handler
        print('Connected to %s' % str(self.address))

    def run(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            message = _messages.decode(data)
            if isinstance(message, _messages.RequestReturnMessage):
                return_message = self.message_handler._search_returned_messages(
                    message.message,
                )
                self.sock.sendall(return_message.encode())
            else:
                self.message_handler._process_message(message)
                self.sock.sendall(_messages.EmptyMessage().encode())


def main(cfg):

    host = cfg['address']
    port = cfg['port']

    message_handler = _MessageHandler()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    while True:
        sock.listen()
        clientsock, clientaddress = sock.accept()
        newthread = ClientThread(
            clientsock,
            clientaddress,
            message_handler,
        )
        newthread.start()


