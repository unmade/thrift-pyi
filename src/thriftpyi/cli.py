import click
from thriftpyi.main import thriftpyi


@click.command()
def main():
    thriftpyi()
