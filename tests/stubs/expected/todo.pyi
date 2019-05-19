from typing import *

from . import shared


class Todo:
    def create(
        self,
        text: str,
    ) -> None:
        ...

    def ping(
        self,
    ) -> str:
        ...
