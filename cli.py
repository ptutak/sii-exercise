import os
import re
from typing import Any

import click
import yaml
from cerberus import Validator


class Element:
    VARIABLE_PATTERN = re.compile(r"\$[A-Za-z_]+")

    def __init__(self, element: Any):
        self._attributes = {}
        self._iterables = []
        self._value = None
        if isinstance(element, dict):
            self._attributes.update(
                {key: Element(value) for key, value in element.items()}
            )
        elif isinstance(element, list):
            self._iterables = [Element(value) for value in element]
        else:
            self._value = element

    def __getattr__(self, attribute: str) -> Any:
        if attribute not in self._attributes:
            raise AttributeError(f"Attribute: {attribute}")
        return self._attributes[attribute]

    def __getitem__(self, index: int) -> Any:
        return self._iterables[index]

    @property
    def value(self) -> Any:
        if isinstance(self._value, str):
            self_value = self._value
            for item in self.VARIABLE_PATTERN.finditer(self._value):
                variable = item.group(0).replace("$", "")
                env_variable = os.getenv(variable)
                if env_variable is not None:
                    self_value = self_value.replace(f"${variable}", env_variable)
            return self_value
        return self._value

    def __str__(self) -> str:
        if self._attributes:
            attrs_str = ", ".join(
                f"{key}={value}" for key, value in self._attributes.items()
            )
            return f"Element({attrs_str})"
        if self._iterables:
            items_str = ", ".join([str(item) for item in self._iterables])
            return f"Element([{items_str}])"
        return f"{self.value}"


@click.command()
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

    validator = Validator(schema_content)
    result = validator.validate(config_content)
    print("Validate result:", result)

    if not result:
        print(validator.errors)
        exit(1)

    config = Element(config_content)
    print(config)
    print(str(config.version))
    print(str(config.workflows))
    print(config.workflows.build_and_test)
    print(config.jobs.build.docker[0].auth.password)


if __name__ == "__main__":
    execute()
