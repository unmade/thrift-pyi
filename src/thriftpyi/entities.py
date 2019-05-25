from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Field:
    name: str
    type: str
    value: Optional[str] = None


@dataclass
class Method:
    name: str
    args: List[Field]
    return_type: Optional[str]


@dataclass
class Service:
    name: str
    methods: List[Method]


@dataclass
class Class:
    name: str
    fields: List[Field]


@dataclass
class Content:
    imports: List[str] = field(default_factory=list)
    errors: List[Class] = field(default_factory=list)
    enums: List[Class] = field(default_factory=list)
    structs: List[Class] = field(default_factory=list)
    services: List[Service] = field(default_factory=list)
    is_async: bool = False
