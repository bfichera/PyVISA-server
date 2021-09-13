from runpy import run_path
from pathlib import Path
from appdirs import user_config_dir


def _get_knownclasses_path(path=None):
    if not path:
        return (
            Path(
                user_config_dir('pyvisa-server'),
            ) / 'known_classes.py'
        ).absolute()
    else:
        return Path(path).absolute()


def _get_knownclasses(path):
    if not path:
        path = _get_knownclasses_path(path)
    known_classes = run_path(
        _get_knownclasses_path(path),
    )['known_classes']
    return known_classes
