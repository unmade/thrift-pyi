from thriftpyi import files, renderers


def thriftpyi():
    result = renderers.render()
    files.save(result, to="tests/stubs/actual/todo.pyi")
