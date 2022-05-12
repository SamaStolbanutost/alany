#!/usr/bin/python3
import sys
from .cli.alany import *
from .cli.esobyte import *
from .cli.main import cli

if __name__ == '__main__':
    args = sys.argv
    if '--help' in args or len(args) == 1:
        print('Alany 0.0.8')
        print('')
    cli()