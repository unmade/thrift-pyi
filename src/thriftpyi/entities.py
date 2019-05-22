from dataclasses import dataclass, field
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
    value: Optional[str]


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
    imports: List[str] = field(default_factory=list)
    errors: List[Error] = field(default_factory=list)
    enums: List[Enumeration] = field(default_factory=list)
    structs: List[Struct] = field(default_factory=list)
    services: List[Service] = field(default_factory=list)
