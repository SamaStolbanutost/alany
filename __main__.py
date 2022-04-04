import sys
import click
from main import run_file

@click.group()
@click.version_option("0.0.1")
def cli():
    pass

@cli.command()
@click.argument('file')
def run(file):
    run_file(file)

if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("Alany")
    cli()