# -*- coding: utf-8 -*-
import os
import subprocess
from enum import Enum


class UiExtensions(str, Enum):
    UI = ".ui"
    QRC = ".qrc"


def create_moc(dir_path: str, file_name: str, extension: UiExtensions) -> None:
    input_file = os.path.join(dir_path, file_name)
    output_file = None

    if extension == UiExtensions.UI:
        output_file = os.path.join(dir_path, f"""moc_{(os.path.splitext(file_name)[0])}.py""")
    elif extension == UiExtensions.QRC:
        output_file = os.path.join(dir_path, f"""{(os.path.splitext(file_name)[0])}_rc.py""")

    if os.path.isfile(output_file):
        ui_file_modification_time = os.path.getmtime(input_file)
        moc_file_modification_time = os.path.getmtime(output_file)
        if moc_file_modification_time > ui_file_modification_time:
            print("Skipping mocking of file {}, older than moc file".format(input_file))
            return

    try:
        print("Remove old moc file: %s" % output_file)
        os.remove(output_file)
    except OSError:
        pass

    command = None

    if extension == UiExtensions.UI:
        command = f'pyside6-uic --from-imports "{input_file}"  -o  "{output_file}"'
    elif extension == UiExtensions.QRC:
        command = f'pyside6-rcc "{input_file}"  -o  "{output_file}"'

    print("Mocking file %s..." % input_file)

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output_bin, err_bin) = process.communicate(timeout=10)
    return_code = process.returncode
    if return_code != 0:
        raise Exception(
            "Mocing ui file failed! (" + file_name + "). cout: " + str(output_bin) + ". cerr: " + str(err_bin)
        )


def create_mocs() -> None:
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
        for file in files:
            for extension in UiExtensions:
                if file.endswith(extension):
                    create_moc(root, file, extension)
    print("Mocking finished!")


if __name__ == "__main__":
    create_mocs()
