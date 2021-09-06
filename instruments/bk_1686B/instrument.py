from .conf import cfg

_Subclass = cfg['InstrumentSubclass']
resource_kwargs = cfg['resource_kwargs']

class bk_1686B(_Subclass):

    def write(self, *args, **kwargs):
        print('bk_1686B writing')
        return _Subclass.write(self, *args, **kwargs)

    def read(self, *args, **kwargs):
        print('bk_1686B reading')
        ans = _Subclass.read(self, *args, **kwargs)
        _Subclass.read(self, *args, **kwargs)
        return ans

    def configure(self):
        for k,v in resource_kwargs.items():
            setattr(self, k, v)
