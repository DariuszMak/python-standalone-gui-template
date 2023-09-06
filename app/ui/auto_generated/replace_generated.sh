pyside6-uic --from-imports --output ./app/ui/auto_generated/main_window.py ./app/ui/forms/main_window.ui
pyside6-uic --from-imports --output ./app/ui/auto_generated/warning_dialog.py ./app/ui/forms/warning_dialog.ui

pyside6-rcc --output ./app/ui/auto_generated/files_rc.py ./app/ui/forms/files.qrc
