import logging
from queue import Queue
import threading

import pyvisa

from .._knownclasses import known_classes
from . import _messages
from ._utilities import (
    _check_output,
    _send_message,
)

_logger = logging.getLogger(__name__)


class RemoteInstrument:

    def __init__(self, instrument_name, sock, resource_name=None):
        self.sock = sock
        self.instrument_name = instrument_name
        if resource_name is not None:
            message = _messages.NewInstrumentMessage(self.instrument_name, resource_name)
            _send_message(self.sock, message)

    def __getattr__(self, name):

        message = _messages.GetAttrCallableMessage(self.instrument_name, name)
        _send_message(self.sock, message)

        if not _check_output(self.sock, message):
            message = _messages.GetAttrMessage(self.instrument_name, name)
            _send_message(self.sock, message)
            return _check_output(self.sock, message)

        else:
            def method(*args, **kwargs):
                message = _messages.RunMethodMessage(self.instrument_name, name, *args, **kwargs)
                _send_message(self.sock, message)
                return _check_output(self.sock, message).value

            return method
        

class _InstrumentThread(threading.Thread):

    def __init__(self, instrument, message_handler, queue):
        self.instrument = instrument
        self.message_handler = message_handler
        self.queue = queue
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if not self.queue.empty():
                message = self.queue.get()
                if isinstance(message, _messages.GetAttrMessage):
                    value = getattr(self.instrument, message.name)
                    newmessage = _messages.ReturnAttrMessage(
                        message,
                        value=value,
                    )
                elif isinstance(message, _messages.GetAttrCallableMessage):
                    value = callable(getattr(self.instrument, message.name))
                    newmessage = _messages.ReturnAttrMessage(
                        message,
                        value=value,
                    )
                elif isinstance(message, _messages.RunMethodMessage):
                    method = getattr(self.instrument, message.name)
                    if not callable(method):
                        raise ValueError(
                            'RunMethodMessage used for'
                            ' uncallable object; use GetAttrMessage or'
                            ' SetAttrMessage instead.'
                        )
                    value = method(*message.args, **message.kwargs)
                    newmessage = _messages.ReturnAttrMessage(
                        message,
                        value=value,
                    )
                else:
                    newmessage = _messages.EmptyMessage()
                self.message_handler._process_message(newmessage)
                # TODO
                # if isinstance(message, CloseMessage):
                #     break


class _InstrumentsManager:

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

        if instrument_name not in known_classes.keys():
            _logger.warning(f'Warning: pyclass {resource_pyclass} unknown.')
        setattr(
            self,
            instrument_name,
            _InstrumentThread(
                self.resource_manager.open_resource(
                    resource_name,
                    resource_pyclass=resource_pyclass,
                ),
                self.message_handler,
                Queue(maxsize=1024),
            )
        )
        getattr(self, instrument_name).start()


class _MessageHandler:

    def __init__(self):
        # TODO
        self.instruments_manager = _InstrumentsManager(None, self)
        self.returned__messages = []

    def _add_return_result(self, message):
        if isinstance(message, _messages.ReturnAttrMessage):
            self.returned__messages.append(message)

    def _process_message(self, message):

        if isinstance(message, _messages.Message):

            if isinstance(message, _messages.NewInstrumentMessage):
                if not hasattr(self.instruments_manager, message.instrument_name):
                    self.instruments_manager._attach_resource(
                        message.resource_name,
                        message.instrument_name,
                        resource_pyclass=known_classes[message.instrument_name],
                    )
                else:
                    _logger.debug(
                        'Skipping attachment of %s to resource_manager'
                        ' because it already exists' % message.instrument_name,
                    )

            elif isinstance(message, _messages.ReturnAttrMessage):
                self.returned__messages.append(message)

            else:
                instrument = getattr(self.instruments_manager, message.instrument_name)
                instrument.queue.put(message)

    def _search_returned_messages(self, message):
        for i, returned_message in enumerate(self.returned__messages):
            if returned_message.message == message:
                ans = returned_message
                self.returned__messages.remove(ans)
                return ans
        return _messages.EmptyMessage()
                
