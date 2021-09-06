from time import sleep

from .utilities import (
    get_instrument_cfg,
    instrument,
)

cfg = get_instrument_cfg('bk_1686B')

_Subclass = cfg['InstrumentSubclass']
resource_kwargs = cfg['resource_kwargs']


@instrument(resource_kwargs)
class bk_1686B(_Subclass):

    def write(self, *args, **kwargs):
        sleep(0.1)
        print('bk_1686B writing')
        return _Subclass.write(self, *args, **kwargs)

    def read(self, *args, **kwargs):
        sleep(0.1)
        print('bk_1686B reading')
        ans = _Subclass.read(self, *args, **kwargs)
        sleep(0.1)
        _Subclass.read(self, *args, **kwargs)
        return ans

    def init(self):
        print('bk_1686B initializing')
        self.configure()
