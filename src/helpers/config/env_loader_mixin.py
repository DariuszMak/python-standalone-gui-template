import os
from dataclasses import fields


class EnvLoaderMixin:
    def __post_init__(self) -> None:
        for field in fields(self):
            env_name = field.name.upper()
            raw_value = os.getenv(env_name)

            if raw_value is None:
                continue

            if field.type is int:
                value = int(raw_value)
            elif field.type is bool:
                value = raw_value.lower() in {"1", "true", "yes"}
            else:
                value = raw_value

            object.__setattr__(self, field.name, value)
