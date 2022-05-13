import click
from ..compiler import Compiler
from .main import cli

@cli.command()
@click.argument('file', default='')
@click.option('--code', '-c', default='')
def run(file, code):
    if not file == '':
        Compiler().run_file(file)
    elif not code == '':
        Compiler().run(code=code, file='/')