#!/usr/bin/python3
import sys
from .cli.alany import run as rn  # noqa
from .cli.esobyte import esobyte, run  # noqa
from .cli.pia import install, update, remove # noqa
from .cli.main import cli

args = sys.argv
if '--help' in args or len(args) == 1:
    print('Alany 0.0.8')
    print('')
cli()
