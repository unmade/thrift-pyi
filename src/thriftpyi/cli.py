import click

from thriftpyi.main import thriftpyi


@click.command()
@click.argument("interfaces_dir", type=click.Path(exists=True))
@click.option("--output", "-o", help="Directory where to save generated `.pyi` files")
@click.option(
    "--async",
    "is_async",
    is_flag=True,
    help="Whether service methods should be async or not",
)
@click.option(
    "--strict-optional",
    is_flag=True,
    help="If not specified all fields will be optional with default to None",
)
def main(interfaces_dir: str, output: str, is_async: bool, strict_optional: bool):
    thriftpyi(interfaces_dir, output, is_async, strict_optional)
