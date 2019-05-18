from thriftpyi import files, renderers


def thriftpyi(interfaces_dir: str, output_dir: str) -> None:
    interfaces = files.list_interfaces(interfaces_dir)
    for interface in interfaces:
        result = renderers.render()
        files.save(result, to=files.build_output_path(interface, output_dir))
