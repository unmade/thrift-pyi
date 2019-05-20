from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Arg:
    name: str
    type: str


@dataclass
class Method:
    name: str
    args: List[Arg]
    return_type: Optional[str]


@dataclass
class Service:
    name: str
    methods: List[Method]


@dataclass
class Field:
    name: str
    type: str


@dataclass
class Error:
    name: str
    fields: List[Field]


@dataclass
class EnumField:
    name: str
    value: int


@dataclass
class Enumeration:
    name: str
    fields: List[EnumField]


@dataclass
class Struct:
    name: str
    fields: List[Field]


@dataclass
class Content:
    imports: List[str]
    errors: List[Error]
    enums: List[Enumeration]
    structs: List[Struct]
    service: Optional[Service]
