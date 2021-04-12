from typing import Any

import click
import yaml
from cerberus import Validator

from .element import Element


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--config",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Config file",
)
@click.option(
    "--schema",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Schema file",
)
def validate(config: str, schema: str) -> None:
    with open(config) as config_file:
        config_content = yaml.safe_load(config_file)
    with open(schema) as schema_file:
        schema_content = yaml.safe_load(schema_file)
    validate_command(config_content, schema_content)


def validate_command(config_content: Any, schema_content: Any) -> None:
    validator = Validator(schema_content)
    result = validator.validate(config_content)

    print("Validate result: ", result)
    if not result:
        print("Errors:")
        print(validator.errors)
        exit(1)


@cli.command()
@click.option(
    "--config",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Config file",
)
@click.option(
    "--schema",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Schema file",
)
def execute(config: str, schema: str) -> None:
    with open(config) as config_file:
        config_content = yaml.safe_load(config_file)
    with open(schema) as schema_file:
        schema_content = yaml.safe_load(schema_file)
    validate_command(config_content, schema_content)
    execute_command(config_content)


def execute_command(config_content: Any) -> None:
    config = Element(config_content)
    print(config)
    print(str(config.version))
    print(str(config.workflows))
    print(config.workflows.build_and_test)
    print(config.jobs.build.docker[0].auth.password)


if __name__ == "__main__":
    execute()
