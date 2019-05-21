import filecmp
import shutil

from thriftpyi.main import thriftpyi


def test_thriftpyi():
    output_dir = "tests/stubs/actual"
    thriftpyi("example/interfaces", output_dir)
    pyi_files = ["__init__.pyi", "dates.pyi", "shared.pyi", "todo.pyi", "todo_v2.pyi"]
    match, mismatch, errors = filecmp.cmpfiles(
        output_dir, "tests/stubs/expected", pyi_files
    )
    assert errors == []
    assert mismatch == [], "\n\n".join(
        [open(f"{output_dir}/{file}").read() for file in mismatch]
    )
    assert match == pyi_files
    shutil.rmtree("tests/stubs/actual/")
