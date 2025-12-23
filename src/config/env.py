import os
from dataclasses import fields


class EnvLoaderMixin:
    @classmethod
    def from_env(cls):
        kwargs = {}

        for field in fields(cls):
            env_name = field.name.upper()
            raw_value = os.getenv(env_name)

            if raw_value is None:
                kwargs[field.name] = field.default
                continue

            if field.type is int:
                kwargs[field.name] = int(raw_value)
            elif field.type is bool:
                kwargs[field.name] = raw_value.lower() in {"1", "true", "yes"}
            else:
                kwargs[field.name] = raw_value

        return cls(**kwargs)
