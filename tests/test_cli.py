import ast
import filecmp
import shutil
from pathlib import Path

import pytest

from thriftpyi.cli import main


@pytest.mark.parametrize(
    "expected_dir,args",
    [
        ("tests/stubs/expected/sync", ["--strict-optional"]),
        ("tests/stubs/expected/async", ["--async", "--strict-optional"]),
        ("tests/stubs/expected/optional", []),
        ("tests/stubs/expected/frozen", ["--frozen"]),
        ("tests/stubs/expected/kw_only", ["--kw-only"]),
        ("tests/stubs/expected/frozen_kw_only", ["--frozen", "--kw-only"]),
        (
            "tests/stubs/expected/frozen_kw_only_sync",
            ["--frozen", "--kw-only", "--strict-optional"],
        ),
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

    # Validate that all generated files are syntactically valid Python
    for pyi_file in pyi_files:
        file_path = Path(output_dir) / pyi_file
        with open(file_path) as f:
            content = f.read()
            try:
                ast.parse(content)
            except SyntaxError as e:
                pytest.fail(f"Generated file {pyi_file} has invalid Python syntax: {e}")

    # Check that files match expected output
    match, mismatch, errors = filecmp.cmpfiles(output_dir, expected_dir, pyi_files)
    assert errors == []
    assert mismatch == []
    assert match == pyi_files
    shutil.rmtree(output_dir)
