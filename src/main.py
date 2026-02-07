import os
import sys
import threading

from src import application, gui_setup
from src.api.app import run_api
from src.helpers.setup_logging import setup_logging
from src.ui.panel_ui.server import start_panel_in_background
from src.ui.react_ui.server import start_react_ui_in_background

TRUE_ENV_VARIABLES_VALUES = "true", "1", "t"

setup_logging()

if __name__ == "__main__":
    if not (getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")):
        gui_setup.create_mocs()

    if os.getenv("DOCKER_RUNTIME", "False").lower() not in TRUE_ENV_VARIABLES_VALUES:
        threading.Thread(target=run_api, daemon=True).start()
        start_panel_in_background()
        start_react_ui_in_background()


        application.run()
