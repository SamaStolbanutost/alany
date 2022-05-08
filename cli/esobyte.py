import click
from esobyte import compiler
from cli.main import cli

@cli.group()
@click.version_option('EsoByte 0.0.1')
def esobyte():
    pass

@esobyte.command()
@click.argument('file')
def run(file):
    compiler.run_file(file)