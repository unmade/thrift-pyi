from __future__ import annotations

import argparse
from pathlib import Path

from thriftpyi.main import thriftpyi


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("interfaces_dir")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_dir",
        type=Path,
        help="Directory where to save generated `.pyi` files",
    )
    parser.add_argument(
        "--async",
        dest="is_async",
        action="store_true",
        help="Whether service methods should be async or not",
    )
    parser.add_argument(
        "--strict-optional",
        dest="strict_optional",
        action="store_true",
        help="If not specified all fields will be optional with default to None",
    )
    parser.add_argument(
        "--frozen",
        dest="frozen",
        action="store_true",
        help="Whether to generate frozen dataclasses",
    )
    parser.add_argument(
        "--kw-only",
        dest="kw_only",
        action="store_true",
        help="Whether to generate kw_only dataclasses",
    )
    return parser


def main(argv=None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)
    thriftpyi(
        interfaces_dir=args.interfaces_dir,
        output_dir=args.output_dir,
        is_async=args.is_async,
        strict_fields=args.strict_optional,
        strict_methods=True,
        frozen=args.frozen,
        kw_only=args.kw_only,
    )
    return 0
