# -*- coding: utf-8 -*-
"""Main module."""
import os

from app import application

TRUE_ENV_VARIABLES_VALUES = "true", "1", "t"

if __name__ == "__main__":
    if not os.getenv("DOCKER_RUNTIME", "False").lower() in TRUE_ENV_VARIABLES_VALUES:
        application.run()
