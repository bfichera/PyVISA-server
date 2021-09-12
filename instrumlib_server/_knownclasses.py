from runpy import run_path
from pathlib import Path
from appdirs import user_config_dir


def _get_knownclasses_path():
    return Path(
        user_config_dir('instrumlib-server') / 'known_classes.py'
    )


known_classes = run_path(_get_knownclasses_path())['known_classes']
