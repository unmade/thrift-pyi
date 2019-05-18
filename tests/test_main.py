import filecmp

from thriftpyi.main import thriftpyi


def test_thriftpyi():
    thriftpyi()
    match, mismatch, errors = filecmp.cmpfiles(
        "tests/stubs/actual", "tests/stubs/expected", ["todo.pyi"]
    )
    assert match == ["todo.pyi"]
    assert mismatch == []
    assert errors == []
