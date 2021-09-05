import pyvisa
from instruments.instrument import open_instrument
from instruments.bk_1686B import bk_1686B

rm = pyvisa.ResourceManager()
bk = open_instrument(
    'ASRL/dev/ttyUSB0::INSTR',
    rm,
    bk_1686B,
    write_termination='\r',
    read_termination='\r',
)
print(bk.query('GETS'))
