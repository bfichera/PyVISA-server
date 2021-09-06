import pyvisa
from instruments.bk_1686B.instrument import bk_1686B, resource_kwargs

print(bk_1686B)

rm = pyvisa.ResourceManager()
bk = rm.open_resource(
    'ASRL/dev/ttyUSB0::INSTR',
    resource_pyclass=bk_1686B,
)
bk.configure()
bk.write('GETS')
print(bk.read())
