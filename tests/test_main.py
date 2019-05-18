import filecmp
import shutil

from thriftpyi.main import thriftpyi


def test_thriftpyi():
    thriftpyi("example/interfaces", "tests/stubs/actual/")
    pyi_files = ["shared.pyi", "todo.pyi"]
    match, mismatch, errors = filecmp.cmpfiles(
        "tests/stubs/actual", "tests/stubs/expected", pyi_files
    )
    assert match == pyi_files
    assert mismatch == []
    assert errors == []
    shutil.rmtree("tests/stubs/actual/")
