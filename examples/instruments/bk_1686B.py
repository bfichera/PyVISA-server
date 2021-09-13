from time import sleep
from pprint import pformat

from instrumentslib import (
    get_instrument_cfg,
    instrument,
)

cfg = get_instrument_cfg('bk_1686B')

_Parent = cfg['InstrumentParentClass']
resource_kwargs = cfg['resource_kwargs']


@instrument(resource_kwargs, 'bk_1686B')
class bk_1686B(_Parent):

    def write(self, *args, **kwargs):
        sleep(0.1)
        return _Parent.write(self, *args, **kwargs)

    def read(self, *args, **kwargs):
        sleep(0.1)
        ans = _Parent.read(self, *args, **kwargs)
        sleep(0.1)
        _Parent.read(self, *args, **kwargs)
        return ans

    def init(self):
        self.configure()
        self.initialized = True
