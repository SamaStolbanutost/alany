#!/usr/bin/python3
import sys
from alany.cli.alany import run as rn  # noqa
from alany.cli.esobyte import esobyte, run  # noqa
from alany.cli.pia import install, update, remove # noqa
from alany.cli.main import cli


def main():
    args = sys.argv
    if '--help' in args or len(args) == 1:
        print('Alany 0.1.2')
        print('')
    cli()


if __name__ == '__main__':
    main()
