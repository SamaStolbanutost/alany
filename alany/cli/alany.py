import click
from ..compiler import Compiler
from ..interpreter import Interpreter
from .main import cli

@cli.command()
@click.argument('file', default='')
@click.option('--code', '-c', default='')
@click.option('--interactive', '-i', default=True, type=bool)
def run(file, code, interactive):
    if not file == '':
        Compiler().run_file(file)
    elif not code == '':
        Compiler().run(code=code, file='/')
    elif interactive == True:
        Interpreter().run()