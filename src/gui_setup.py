import logging
import os
import subprocess
from enum import Enum

logger = logging.getLogger(__name__)


class UiExtensions(str, Enum):
    UI = ".ui"
    QRC = ".qrc"


def create_moc(dir_path: str, file_name: str, extension: UiExtensions) -> None:
    input_file = os.path.join(dir_path, file_name)
    output_file = None

    if extension == UiExtensions.UI:
        output_file = os.path.join(dir_path, f"moc_{os.path.splitext(file_name)[0]}.py")
    elif extension == UiExtensions.QRC:
        output_file = os.path.join(dir_path, f"{os.path.splitext(file_name)[0]}_rc.py")

    if os.path.isfile(output_file):
        ui_file_modification_time = os.path.getmtime(input_file)
        moc_file_modification_time = os.path.getmtime(output_file)
        if moc_file_modification_time > ui_file_modification_time:
            logger.info("Skipping mocking of file %s, older than moc file", input_file)
            return

    try:
        logger.info("Remove old moc file: %s", output_file)
        os.remove(output_file)
    except OSError:
        pass


    if extension == UiExtensions.UI:
        command = ["pyside6-uic", "--from-imports", input_file, "-o", output_file]
    elif extension == UiExtensions.QRC:
        command = ["pyside6-rcc", input_file, "-o", output_file]

    logger.info("Mocking file %s...", input_file)

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output_bin, err_bin) = process.communicate(timeout=10)
    return_code = process.returncode
    if return_code != 0:
        raise Exception(
            "Mocing ui file failed! (" + file_name + "). cout: " + str(output_bin) + ". cerr: " + str(err_bin)
        )


def create_mocs() -> None:
    for root, _dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
        for file in files:
            for extension in UiExtensions:
                if file.endswith(extension):
                    create_moc(root, file, extension)
    logger.info("Mocking finished!")


if __name__ == "__main__":
    create_mocs()
