import logging
from queue import Queue
import threading

import dill as pickle
import pyvisa

from ..knownclasses import knownclasses
from .messages import (
    NewInstrumentMessage,
    GetAttrMessage,
    SetAttrMessage,
    ReturnAttrMessage,
    # TODO
    # CloseMessage,
    Message,
    EmptyMessage,
    RunMethodMessage,
)

_logger = logging.getLogger(__name__)


class A:

    def __init__(self, val=3):
        self.val = val
        self.val2 = val**2

    def ask(self):
        return self.val+4

    def tell(self, g):
        return self.val + g


class ServerA:

    def __init__(self, sock, instrument_name):
        self.sock = sock
        self.instrument_name = instrument_name

    def __getattr__(self, name):
        data = GetAttrMessage(self.instrument_name, name)
        self.sock.sendall(
            pickle.dumps(data),
        )
        out = self.sock.recv(1024)
        return pickle.loads(out)


class InstrumentThread:

    def __init__(self, instrument, message_handler, queue):
        self.instrument = instrument
        self.message_handler = message_handler
        self.queue = queue

    def poll(self):
        while True:
            if not self.queue.empty():
                message = self.queue.get()
                if isinstance(message, GetAttrMessage):
                    value = getattr(self.instrument, message.name)
                    if callable(value):
                        raise ValueError(
                            'GetAttrMessage used for'
                            'callable method; use RunMethodMessage instead.'
                        )
                    newmessage = ReturnAttrMessage(
                        message,
                        value=value,
                    )
                elif isinstance(message, RunMethodMessage):
                    method = getattr(self.instrument, message.name)
                    if not callable(method):
                        raise ValueError(
                            'RunMethodMessage used for'
                            ' uncallable object; use GetAttrMessage or'
                            ' SetAttrMessage instead.'
                        )
                    value = method(*message.args, **message.kwargs)
                    newmessage = ReturnAttrMessage(
                        message,
                        value=value,
                    )
                else:
                    newmessage = EmptyMessage()
                self.message_handler.process_message(newmessage)
                # TODO
                # if isinstance(message, CloseMessage):
                #     break


class InstrumentsManager:

    def __init__(self, resource_manager, message_handler):
        self.instruments = {}
        self.resource_manager = pyvisa.ResourceManager()
        self.message_handler = message_handler

    def _attach_resource(
        self,
        resource_name,
        instrument_name,
        resource_pyclass=None,
        **kwargs,
    ):

        # TODO
        # if resource_pyclass not in knownclasses.keys():
        #     _logger.warning(f'Warning: pyclass {resource_pyclass} unknown.')
        setattr(
            self,
            instrument_name,
            InstrumentThread(
                self.resource_manager.open_resource(
                    resource_name,
                    resource_pyclass=resource_pyclass,
                ),
                self.message_handler,
                Queue(maxsize=1024),
            )
        )
        threading.Thread(target=getattr(self, instrument_name).poll).start()


class MessageHandler:

    def __init__(self):
        # TODO
        self.instruments_manager = InstrumentsManager(None, self)
        self.returned_messages = []

    def add_return_result(self, message):
        if isinstance(message, ReturnAttrMessage):
            self.returned_messages.append(message)

    def process_message(self, message):

        if isinstance(message, Message):

            if isinstance(message, NewInstrumentMessage):
                self.instruments_manager._attach_resource(
                    message.resource_name,
                    message.instrument_name,
                    resource_pyclass=knownclasses[message.instrument_name],
                )

            if isinstance(message, GetAttrMessage):
                instrument = getattr(self.instruments_manager, message.instrument_name)
                instrument.queue.put(message)

            if isinstance(message, SetAttrMessage):
                instrument = getattr(self.instruments_manager, message.instrument_name)
                instrument.queue.put(message)

            if isinstance(message, ReturnAttrMessage):
                self.returned_messages.append(message)

            if isinstance(message, RunMethodMessage):
                instrument = getattr(self.instruments_manager, message.instrument_name)
                instrument.queue.put(message)
                
    def search_returned_messages(self, message):
        for i, returned_message in enumerate(self.returned_messages):
            if returned_message.message == message:
                ans = returned_message
                self.returned_messages.remove(ans)
                return ans
        return EmptyMessage()
                
