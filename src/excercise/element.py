import re
import os
from typing import Any


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
