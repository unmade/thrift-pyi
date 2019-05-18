import filecmp
import shutil

from thriftpyi.main import thriftpyi


def test_thriftpyi():
    thriftpyi("example/interfaces", "tests/stubs/actual/")
    match, mismatch, errors = filecmp.cmpfiles(
        "tests/stubs/actual", "tests/stubs/expected", ["todo.pyi"]
    )
    assert match == ["todo.pyi"]
    assert mismatch == []
    assert errors == []
    shutil.rmtree("tests/stubs/actual/")
