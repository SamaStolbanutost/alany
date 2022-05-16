import click
from ..compiler import Compiler
from ..interpreter import Interpreter
from .main import cli


@cli.command(help='Runs the code.')
@click.argument('file', default='')
@click.option('--code', '-c', default='', help='Code to run.')
@click.option('--interactive', '-i', default=False, type=bool,
              help='Run in interactive mode.')
def run(file, code, interactive):
    if not file == '':
        Compiler().run_file(file)
    elif not code == '':
        Compiler().run(code=code, file='/')
    elif interactive is True:
        Interpreter().run()
