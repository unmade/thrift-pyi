import click
from thriftpyi.main import thriftpyi


@click.command()
@click.argument("interfaces_dir", type=click.Path(exists=True))
@click.option("--output", help="Directory where to save generated `.pyi` files")
def main(interfaces_dir, output):
    thriftpyi(interfaces_dir, output)
