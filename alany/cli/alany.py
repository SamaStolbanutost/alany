import click
from .. import compiler
from .main import cli

@cli.command()
@click.argument('file', default='')
@click.option('--code', '-c', default='')
def run(file, code):
    if not file == '':
        compiler.Compiler().run_file(file)
    elif not code == '':
        compiler.Compiler().run(code=code, file='/')