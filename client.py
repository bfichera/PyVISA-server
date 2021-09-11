import socket
import sys

from instrumlib.server.instrumentmanager import RemoteInstrument

HOST = '127.0.0.1'
PORT = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

bk_1686B = RemoteInstrument('bk_1686B', sock, 'ASRL/dev/ttyUSB0::INSTR')
bk_1686B.init()

while True:
    try:
        print(bk_1686B.query('GETS'))
    except KeyboardInterrupt:
        break

sock.close()
