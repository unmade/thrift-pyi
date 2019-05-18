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
class Content:
    imports: List[str]
    service: Service
