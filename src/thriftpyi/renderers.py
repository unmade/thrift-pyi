from importlib import resources

from jinja2 import Template


def render() -> str:
    template = Template(resources.read_text("thriftpyi.templates", "stub.html"))
    return template.render()
