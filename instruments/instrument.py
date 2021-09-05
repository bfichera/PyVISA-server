import logging
import types
import inspect
import time

_logger = logging.getLogger(__name__)


class _Copy:
    pass


def _modify_resource(resource, template):

    for methodname, method in inspect.getmembers(template):
        if not methodname.startswith('__'):
            copy = _Copy()
            try: 
                def func(self, *args, **kwargs):
                    return method(self, copy, *args, **kwargs)
                setattr(copy, methodname, getattr(resource, methodname))
                setattr(resource, methodname, types.MethodType(func, resource))
            except:
                pass

def open_instrument(resource_name, resource_manager, template, *args, **kwargs):
    resource = resource_manager.open_resource(resource_name, *args, **kwargs)
    _modify_resource(resource, template)
    return resource
