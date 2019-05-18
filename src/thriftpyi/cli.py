import click
from thriftpyi.main import thriftpyi


@click.command()
@click.option("--interfaces", help="Directory with thrift interfaces")
@click.option("--output", help="Directory where to save generated `.pyi` files")
def main(interfaces, output):
    thriftpyi(interfaces, output)
