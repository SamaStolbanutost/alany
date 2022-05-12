import click
from .. import compiler
from .main import cli

@cli.command()
@click.argument('file')
def run(file):
    compiler.Compiler().run_file(file)