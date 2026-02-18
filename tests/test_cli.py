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
    "input_dir,args,test_code",
    [
        (
            "example/interfaces",
            ["--frozen"],
            "from generated import todo\ntodo.TodoItem()",
        ),
        pytest.param(
            "example/interfaces",
            ["--frozen", "--kw-only"],
            "from generated import todo\ntodo.TodoItem()",
            marks=pytest.mark.skipif(
                sys.version_info < (3, 10), reason="kw_only requires Python 3.10+"
            ),
        ),
        (
            "tests/cross_dir_interfaces",
            ["--frozen"],
            "from generated import parent\nparent.ParentRecord()",
        ),
    ],
)
def test_generated_code_is_importable(tmp_path, input_dir, args, test_code):
    output_dir = tmp_path / "generated"

    main([input_dir, "--output", str(output_dir), *args])

    for pyi_file in output_dir.glob("*.pyi"):
        pyi_file.with_suffix(".py").write_text(pyi_file.read_text())
    (output_dir / "__init__.py").write_text("")

    test_script = tmp_path / "test_import.py"
    test_script.write_text(
        f"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
{test_code}
print("Success")
"""
    )

    result = subprocess.run(
        [sys.executable, str(test_script)], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, f"Failed to run generated code: {result.stderr}"
    assert "Success" in result.stdout


def test_cross_dir_includes(tmp_path):
    output_dir = tmp_path / "stubs"

    main(
        ["tests/cross_dir_interfaces", "--output", str(output_dir), "--strict-optional"]
    )

    pyi_files = ["__init__.pyi", "_typedefs.pyi", "child.pyi", "parent.pyi"]
    match, mismatch, errors = filecmp.cmpfiles(
        str(output_dir), "tests/stubs/expected/cross_dir", pyi_files
    )
    assert errors == []
    assert mismatch == []
    assert match == pyi_files
