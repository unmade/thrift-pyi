import filecmp
import shutil

import pytest

from thriftpyi.cli import main


@pytest.mark.parametrize(
    "expected_dir,args",
    [
        ("tests/stubs/expected/sync", ["--strict-optional"]),
        ("tests/stubs/expected/async", ["--async", "--strict-optional"]),
        ("tests/stubs/expected/optional", []),
    ],
)
def test_main(capsys, expected_dir, args):
    del capsys

    input_dir = "example/interfaces"
    output_dir = "tests/stubs/actual"

    main([input_dir, "--output", output_dir, *args])

    pyi_files = [
        "__init__.pyi",
        "_typedefs.pyi",
        "dates.pyi",
        "shared.pyi",
        "todo.pyi",
        "todo_v2.pyi",
    ]
    match, mismatch, errors = filecmp.cmpfiles(output_dir, expected_dir, pyi_files)
    assert errors == []
    assert mismatch == []
    assert match == pyi_files
    shutil.rmtree(output_dir)
