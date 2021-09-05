import logging

from pyvisa.errors import VisaIOError

_logger = logging.getLogger(__name__)


class Instrument:

    def __init__(self, resource, **kws):
        self._resource = resource
        for k,v in kws.items():
            self._resource.__setattr__(k, v)

    def configure(self, **kws):
        
