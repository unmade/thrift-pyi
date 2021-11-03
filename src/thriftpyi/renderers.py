from dataclasses import asdict
from importlib import resources

from jinja2 import Template

from thriftpyi.entities import Content


def render(content: Content) -> str:
    template = Template(resources.read_text("thriftpyi.templates", "stub.html"))
    return template.render(**asdict(content))  # type: ignore
