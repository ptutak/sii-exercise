import os.path

from click.testing import CliRunner
from pytest import fixture

from exercise.cli import cli


@fixture
def test_files_dir():
    return os.path.join(os.path.dirname(__file__), "test_files")


def test_validate(test_files_dir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "validate",
            "--config",
            os.path.join(test_files_dir, "config.yml"),
            "--schema",
            os.path.join(test_files_dir, "schema.yml"),
        ],
    )

    assert result.exit_code == 0
    assert result.output == "Validate result: True\n"


def test_validate_wrong(test_files_dir):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "validate",
            "--config",
            os.path.join(test_files_dir, "wrong-config.yml"),
            "--schema",
            os.path.join(test_files_dir, "schema.yml"),
        ],
    )

    assert result.exit_code == 1
    assert (
        result.output
        == """Validate result: False
Errors:
{'jobs': [{0: [{'dockerd': ['unknown field']}]}]}
"""
    )


def test_execute(test_files_dir):
    runner = CliRunner()
    result = runner.invoke(
        cli, ["execute", "--config", os.path.join(test_files_dir, "config.yml")]
    )

    assert result.exit_code == 0
    assert (
        result.output
        == """2.1.1
Element([Element(name=build_and_test, jobs=Element([build, test]))])
Element(name=build_and_test, jobs=Element([build, test]))
$DOCKERHUB_PASSWORD
"""
    )
