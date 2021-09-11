from . import _messages
import dill as pickle


def _check_output(sock, original_message):
    returned_message = _messages.EmptyMessage()
    while isinstance(returned_message, _messages.EmptyMessage):
        check_message = _messages.RequestReturnMessage(original_message)
        sock.sendall(pickle.dumps(check_message))
        data = sock.recv(1024)
        returned_message = pickle.loads(data)
    return returned_message


def _send_message(sock, message):
    sock.sendall(message.encode())
    sock.recv(1024)
