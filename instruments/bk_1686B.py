def instrument(cls):

    def make_init(old_init):

        def new_init(self, resource_name, resource_manager, *args, **kwargs):
            self._resource = resource_manager.open_resource(resource_name)
            for k,v in kwargs.items():
                self._resource.__setattr__(k, v)
            for name in dir(self._resource):
                if name not in dir(self):
                    val = getattr(self._resource, name)
                    if callable(val):
                        if 'self' in inspect.signature(val).parameters.keys():
                            def new_func(obj, *args, **kwargs):
                                return val(self, *args, **kwargs)
                            setattr(self, name, new_func)
                        else:
                            setattr(self, name, f)
                    try:
                        setattr(self, name, getattr(self._resource, name))
                    except:
                        pass

        return new_init

    if cls.__init__ != object.__init__:
        raise ValueError('defining __init__ in object %s not allowed with @instrument' % cls)

    cls.__init__ = make_init(cls.__init__)
    return cls

@instrument
class bk_1686B:
    
    def write(self, *args, **kwargs):
        print('fuck you!')
        return self._resource.write(*args, **kwargs)
