import os
import sys
import threading

from src import application, gui_setup
from src.api_runner import run_api

TRUE_ENV_VARIABLES_VALUES = "true", "1", "t"

if __name__ == "__main__":
    if not (getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")):
        gui_setup.create_mocs()

    if os.getenv("DOCKER_RUNTIME", "False").lower() not in TRUE_ENV_VARIABLES_VALUES:
        threading.Thread(target=run_api, daemon=True).start()
        application.run()
