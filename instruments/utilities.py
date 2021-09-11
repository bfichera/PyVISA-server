import json
from pathlib import Path
from runpy import run_path
import logging

from appdirs import user_config_dir

_logger = logging.getLogger(__name__)


_default_protected_config = r"""import pyvisa

cfg = {
    'InstrumentSubclass':pyvisa.resources.serial.SerialInstrument,
}
"""

_default_unprotected_config = r"""{
    "lock":false,
    "resource_kwargs":{
    }
}
"""


def instrument(resource_kwargs, instrument_name):

    conf_unprotected_filename = _get_unprotected_config_path(instrument_name)
    _open = open

    def decorator(cls):

        class newcls(cls):

            def configure(self):
                for k,v in resource_kwargs.items():
                    setattr(self, k, v)

            @property
            def lock(self):
                return self._get_cfg_attr('lock')

            @lock.setter
            def lock(self, value):
                self._set_cfg_attr('lock', value)

            def open(self, *args, **kwargs):
                if self.lock is True:
                    raise ValueError('Instrument %s locked.' % instrument_name)
                else:
                    self.lock = True
                return cls.open(self, *args, **kwargs)

            def close(self, *args, **kwargs):
                self.lock = False
                return cls.close(self, *args, **kwargs)

            def _get_cfg_attr(self, name):
                with _open(conf_unprotected_filename, 'r') as fh:
                    cfg = json.load(fh)
                return cfg[name]

            def _set_cfg_attr(self, name, value):
                with _open(conf_unprotected_filename, 'r') as fh:
                    cfg = json.load(fh)
                if name in cfg.keys():
                    cfg[name] = value
                else:
                    raise ValueError(
                        'Can\'t create new attribute automatically; set a'
                        'default value in the relevant config file',
                    )
                with _open(conf_unprotected_filename, 'w') as fh:
                    json.dump(cfg, fh)
                
#             cls.configure = configure
#             cls.lock = lock
#             cls.open = open
#             cls.close = close
#             cls._get_cfg_attr = _get_cfg_attr
#             cls._set_cfg_attr = _set_cfg_attr
        return newcls

    return decorator


def _get_protected_config_path(instrument_name):
    return Path(
        user_config_dir('instruments'),
    ) / instrument_name / 'conf-protected.py'


def _get_unprotected_config_path(instrument_name):
    return Path(
        user_config_dir('instruments'),
    ) / instrument_name / 'conf.json'


def get_instrument_cfg(instrument_name):
    """Retrieves instrument configuration files from default filepaths.
    Creates the file if it doesn't exist.

    Parameters
    ----------
    instrument_name : str

    Returns
    -------
    cfg : dict
    """

    protected_config_path = _get_protected_config_path(instrument_name)
    unprotected_config_path = _get_unprotected_config_path(instrument_name)

    for i, fp in enumerate((protected_config_path, unprotected_config_path)):
        if not fp.exists():
            _logger.warning('No config file found. Creating default config file at %s' % fp.as_posix())
            if not fp.parent.exists():
                fp.parent.mkdir(parents=True)
            with open(fp, 'w') as fh:
                file_strs = [
                    _default_protected_config,
                    _default_unprotected_config,
                ]
                fh.write(file_strs[i])
                
    conf_protected = run_path(protected_config_path)['cfg']
    with open(unprotected_config_path, 'r') as fh:
        conf_unprotected = json.load(fh)

    cfg = {}
    for dict in [conf_protected, conf_unprotected]:
        for k,v in dict.items():
            if k in cfg.keys():
                raise ValueError(
                    'Conflicting config values in %s and %s'
                    % (
                        protected_config_path,
                        unprotected_config_path,
                    ),
                )
            cfg[k] = v

    return cfg
