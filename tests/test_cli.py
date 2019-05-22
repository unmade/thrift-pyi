import filecmp
import shutil

from click.testing import CliRunner
from thriftpyi.cli import main


def test_main():
    input_dir = "example/interfaces"
    output_dir = "tests/stubs/actual"
    expected_dir = "tests/stubs/expected"
    pyi_files = ["__init__.pyi", "dates.pyi", "shared.pyi", "todo.pyi", "todo_v2.pyi"]
    runner = CliRunner()

    result = runner.invoke(main, ["--interfaces", input_dir, "--output", output_dir])
    assert result.exit_code == 0

    match, mismatch, errors = filecmp.cmpfiles(output_dir, expected_dir, pyi_files)
    assert errors == []
    assert mismatch == []
    assert match == pyi_files
    shutil.rmtree(output_dir)
