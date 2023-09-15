# -*- coding: utf-8 -*-
"""Main module."""
import os

from src import application, gui_setup

TRUE_ENV_VARIABLES_VALUES = "true", "1", "t"

if __name__ == "__main__":
    gui_setup.create_mocs()
    if not os.getenv("DOCKER_RUNTIME", "False").lower() in TRUE_ENV_VARIABLES_VALUES:
        application.run()
