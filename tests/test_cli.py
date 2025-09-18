import filecmp
import shutil
import subprocess
import sys

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

    # Check that files match expected output
    match, mismatch, errors = filecmp.cmpfiles(output_dir, expected_dir, pyi_files)
    assert errors == []
    assert mismatch == []
    assert match == pyi_files
    shutil.rmtree(output_dir)


@pytest.mark.parametrize(
    "args",
    [
        ["--frozen"],
        pytest.param(
            ["--frozen", "--kw-only"],
            marks=pytest.mark.skipif(
                sys.version_info < (3, 10), reason="kw_only requires Python 3.10+"
            ),
        ),
    ],
)
def test_generated_code_is_importable(tmp_path, args: list[str]):
    # WHEN
    input_dir = "example/interfaces"
    output_dir = tmp_path / "generated"

    # Generate stubs with frozen option (without kw_only)
    main([input_dir, "--output", str(output_dir), *args])

    # Copy .pyi files to .py files so they can be imported
    for pyi_file in output_dir.glob("*.pyi"):
        py_file = pyi_file.with_suffix(".py")
        py_file.write_text(pyi_file.read_text())

    # Create __init__.py to make it a proper package
    (output_dir / "__init__.py").write_text("")

    # Create a test script that imports and uses the generated code
    test_script = tmp_path / "test_import.py"
    test_script.write_text(
        """
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Import the generated package (not individual modules)
from generated import todo

# Try to instantiate TodoItem with defaults
# This will raise NameError if the lambda references undefined DateTime
item = todo.TodoItem()
print("Success: TodoItem instantiated")
"""
    )

    # WHEN
    result = subprocess.run(
        [sys.executable, str(test_script)], capture_output=True, text=True, check=False
    )

    # THEN
    # Check for NameError specifically
    assert result.returncode == 0, f"Failed to run generated code: {result.stderr}"
    assert (
        "NameError" not in result.stderr
    ), f"Generated code has undefined names: {result.stderr}"
    assert "Success" in result.stdout
