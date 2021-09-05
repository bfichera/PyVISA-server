import logging
import pyvisa

from instruments.bk_1686B import bk_1686B

# logging.basicConfig(level=logging.WARNING)

#hi = Resource()
rm = pyvisa.ResourceManager()
me = bk_1686B('ASRL/dev/ttyUSB0::INSTR', rm, write_termination='\r', read_termination='\r')
print(me.query('GETS'))
