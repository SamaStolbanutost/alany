import click
import compiler
from cli.main import cli

@cli.command()
@click.argument('file')
def run(file):
    compiler.Compiler().run_file(file)