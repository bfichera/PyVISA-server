import random


class Message:

    def __init__(self):
        # TODO
        self.id = random.randint(0, 2**128)

    def __eq__(self, other):
        return self.id == other.id


class GetAttrMessage(Message):

    def __init__(self, instrument_name, name):
        self.instrument_name = instrument_name
        self.name = name
        Message.__init__(self)


class RunMethodMessage(Message):

    def __init__(self, instrument_name, name, *args, **kwargs):
        self.instrument_name = instrument_name
        self.name = name
        self.args = args
        self.kwargs = kwargs
        Message.__init__(self)


class SetAttrMessage(Message):

    def __init__(self, instrument_name, name, value):
        self.instrument_name = instrument_name
        self.name = name
        self.value = value
        Message.__init__(self)


class NewInstrumentMessage(Message):

    def __init__(self, instrument_name, resource_name):
        self.instrument_name = instrument_name
        self.resource_name = resource_name
        Message.__init__(self)


class ReturnAttrMessage(Message):

    def __init__(self, message, value):
        self.message = message
        self.value = value
        Message.__init__(self)


class RequestReturnMessage(Message):

    def __init__(self, message):
        self.message = message
        Message.__init__(self)


class EmptyMessage(Message):
    
    def __init__(self):
        Message.__init__(self)


class CloseMessage(Message):

    def __init__(self, instrument_name):
        self.instrument_name = instrument_name
        Message.__init__(self)
