from click.testing import CliRunner
from thriftpyi.cli import main


def test_main(mocker):
    runner = CliRunner()
    thriftpyi_mock = mocker.patch("thriftpyi.cli.thriftpyi")
    result = runner.invoke(
        main, ["--interfaces", "path/to/interfaces", "--output", "output/path"]
    )
    assert thriftpyi_mock.call_args == mocker.call("path/to/interfaces", "output/path")
    assert result.exit_code == 0
