from typing import List

from thriftpyi.entities import Arg, Content, Method, Service


def parse(interface: str) -> Content:
    del interface
    return Content(imports=parse_imports(), service=parse_service())


def parse_imports() -> List[str]:
    return ["shared"]


def parse_service() -> Service:
    return Service(
        name="Todo",
        methods=[
            Method(
                name="create", args=[Arg(name="text", type="str")], return_type="None"
            )
        ],
    )
