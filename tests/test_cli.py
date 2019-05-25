import filecmp
import shutil

import pytest
from click.testing import CliRunner
from thriftpyi.cli import main


@pytest.mark.parametrize(
    "expected_dir,args",
    [("tests/stubs/expected/sync", []), ("tests/stubs/expected/async", ["--async"])],
)
def test_main(expected_dir, args):
    input_dir = "example/interfaces"
    output_dir = "tests/stubs/actual"

    runner = CliRunner()
    result = runner.invoke(main, [input_dir, "--output", output_dir] + args)
    assert result.exit_code == 0

    pyi_files = ["__init__.pyi", "dates.pyi", "shared.pyi", "todo.pyi", "todo_v2.pyi"]
    match, mismatch, errors = filecmp.cmpfiles(output_dir, expected_dir, pyi_files)
    assert errors == []
    assert mismatch == []
    assert match == pyi_files
    shutil.rmtree(output_dir)
