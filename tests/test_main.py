import filecmp
import shutil

from thriftpyi.main import thriftpyi


def test_thriftpyi():
    thriftpyi("example/interfaces", "tests/stubs/actual/")
    pyi_files = ["__init__.pyi", "dates.pyi", "shared.pyi", "todo.pyi", "todo_v2.pyi"]
    match, mismatch, errors = filecmp.cmpfiles(
        "tests/stubs/actual", "tests/stubs/expected", pyi_files
    )
    assert errors == []
    assert mismatch == []
    assert match == pyi_files
    shutil.rmtree("tests/stubs/actual/")
