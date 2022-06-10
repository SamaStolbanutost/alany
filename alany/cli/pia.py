import click
from ..pia import main
from .main import cli


@cli.group(help='Package Installer for Alany')
@click.version_option('Pia 0.0.1')
def pia():
    pass


@pia.command(help='Installs a package from a git repository or from a list.')
@click.argument('name')
def install(name: str):
    if not name == '':
        if name.startswith('http://') or name.startswith('https://') \
                or name.startswith('git@'):
            main.install(name=name.split('/')[-1], link=name)
        else:
            main.install(name=name)


@pia.command(help='Updates a package from a git repository or from a list.')
@click.argument('name', default='')
def update(name: str):
    if not name == '':
        if name.startswith('http://') or name.startswith('https://') \
                or name.startswith('git@'):
            main.update(name=name.split('/')[-1], link=name)
        else:
            main.update(name=name)


@pia.command(help='Removes a package from a git repository or list.')
@click.argument('name', default='')
def remove(name: str):
    if not name == '':
        if name.startswith('http://') or name.startswith('https://') \
                or name.startswith('git@'):
            main.remove(name.split('/')[-1])
        else:
            main.remove(name)
