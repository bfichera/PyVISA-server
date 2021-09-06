import pyvisa
from instruments.bk_1686B import bk_1686B
from pathlib import Path

rm = pyvisa.ResourceManager()
bk = rm.open_resource(
    'ASRL/dev/ttyUSB0::INSTR',
    resource_pyclass=bk_1686B,
)
bk.init()
bk.write('GETS')
print(bk.read())
