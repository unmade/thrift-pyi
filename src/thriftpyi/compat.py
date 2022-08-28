import sys

if sys.version_info < (3, 9):
    import astunparse

    ast_unparse = astunparse.unparse
else:
    import ast

    ast_unparse = ast.unparse  # pylint: disable=no-member
