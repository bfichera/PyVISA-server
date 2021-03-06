import argparse
from pathlib import Path

from appdirs import user_config_dir

from pyvisaserver._startserver import main as startserver_main


def _getcfg():
    parser = argparse.ArgumentParser(description='Start pyvisa server')
    parser.add_argument(
        '-a',
        '--addr',
        dest='address',
        default='127.0.0.1',
    )
    parser.add_argument(
        '-p',
        '--port',
        dest='port',
        type=int,
        default=2264,
    )
    parser.add_argument(
        '-K',
        '--known',
        dest='known_classes_path',
        type=lambda p:Path(p).absolute(),
        default=Path(user_config_dir('pyvisa-server')) / 'known_classes.py',
    )
    args = parser.parse_args()
    return vars(args)


def main():

    cfg = _getcfg()
    startserver_main(cfg)
