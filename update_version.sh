#!/bin/bash

echo $1 > .version
echo -ne "from .instrumentmanager import RemoteInstrument\n__version__ = '$1'\n" > pyvisaserver/__init__.py
