from typing import *


class NotFound(Exception):
    message: Optional[str]


class Service:
    def ping(
        self,
    ) -> str:
        ...
