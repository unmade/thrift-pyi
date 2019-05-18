from thriftpyi.renderers import render


def test_render():
    assert render() == "Hello, World!"
