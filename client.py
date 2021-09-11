import socket
import sys
from info import ServerA


HOST = '127.0.0.1'
PORT = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((HOST, PORT))
servera = ServerA(s, 'b')
print(servera.tell(9))
