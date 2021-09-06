import pyvisa
from pyvisa.resources.serial import SerialInstrument

cfg = {
    'InstrumentSubclass':SerialInstrument,
    'resource_kwargs':{
        'write_termination':'\r',
        'read_termination':'\r',
    },
}
