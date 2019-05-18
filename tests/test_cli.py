from click.testing import CliRunner
from thriftpyi.cli import main


def test_main(mocker):
    runner = CliRunner()
    thriftpyi_mock = mocker.patch("thriftpyi.cli.thriftpyi")
    result = runner.invoke(main, [])
    assert thriftpyi_mock.called
    assert result.exit_code == 0
