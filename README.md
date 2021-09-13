# PyVISA-server

A local server designed to manage communication between clients and multiple different VISA instruments.

### Requirements (minimal)

* [`appdirs`](https://github.com/ActiveState/appdirs)
* [`dill`](https://github.com/uqfoundation/dill)
* [`pyvisa`](https://github.com/pyvisa/pyvisa)
* a `pyvisa` backend (e.g. [`pyvisa-py`](https://github.com/pyvisa/pyvisa-py))
* A `known_classes.py` file (see [examples](examples))

### Requirements (recommended)

* [`InstrumentsLib`](https://github.com/bfichera/InstrumentsLib)

### Usage
```
usage: pyvisa-server [-h] [-a ADDRESS] [-p PORT] [-K KNOWN_CLASSES_PATH]

Start pyvisa server

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --addr ADDRESS
  -p PORT, --port PORT
  -K KNOWN_CLASSES_PATH, --known KNOWN_CLASSES_PATH
```
