import logging
import subprocess  # noqa: S404
from enum import StrEnum
from pathlib import Path

logger = logging.getLogger(__name__)


class UiExtensions(StrEnum):
    UI = ".ui"
    QRC = ".qrc"


def find_project_root(start: Path) -> Path:
    for parent in start.resolve().parents:
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
            return parent
    raise RuntimeError("Project root not found")


PROJECT_ROOT = find_project_root(Path(__file__))


def create_moc(file_path: Path, extension: UiExtensions) -> None:
    input_file = file_path
    output_file: Path | None = None

    if extension == UiExtensions.UI:
        output_file = file_path.with_name(f"moc_{file_path.stem}.py")
    elif extension == UiExtensions.QRC:
        output_file = file_path.with_name(f"{file_path.stem}_rc.py")

    if output_file.exists():
        if output_file.stat().st_mtime > input_file.stat().st_mtime:
            logger.info("Skipping %s (already up to date)", input_file)
            return

    try:
        logger.info("Removing old file: %s", output_file)
        output_file.unlink()
    except FileNotFoundError:
        pass

    if extension == UiExtensions.UI:
        command = [
            "pyside6-uic",
            "--from-imports",  
            str(input_file),
            "-o",
            str(output_file),
        ]
    elif extension == UiExtensions.QRC:
        command = [
            "pyside6-rcc",
            str(input_file),
            "-o",
            str(output_file),
        ]

    logger.info("Generating: %s", input_file)

    process = subprocess.run(  # noqa: S603
        command,
        capture_output=True,
        text=True,
    )

    if process.returncode != 0:
        raise RuntimeError(
            f"Failed for {input_file}\nstdout:\n{process.stdout}\nstderr:\n{process.stderr}"
        )


def create_mocs() -> None:
    for file_path in PROJECT_ROOT.rglob("*"):
        for extension in UiExtensions:
            if file_path.suffix == extension:
                create_moc(file_path, extension)

    logger.info("MOC generation finished!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_mocs()