import logging
import platform
import shutil
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

FRONTEND_DIR: Path = Path(__file__).parent / "ui" / "react_ui" / "frontend"
STATIC_DIR: Path = Path(__file__).parent / "ui" / "react_ui" / "static"
DIST_DIR: Path = FRONTEND_DIR / "dist"

NPM_CMD: str = "npm"
if platform.system() == "Windows":
    NPM_CMD = "npm.cmd"


def run_command(command: list[str], cwd: Path | None = None) -> str:

    logger.info("Running command: %s", " ".join(command))
    if not cwd or not Path(cwd).exists():
        raise NotADirectoryError(f"Directory does not exist: {cwd}")
    process = subprocess.run(command, cwd=cwd, capture_output=True, text=True)  # noqa: S603
    if process.returncode != 0:
        logger.error("Command failed! stdout: %s, stderr: %s", process.stdout, process.stderr)
        raise RuntimeError(f"Command {command} failed")
    return process.stdout


def install_dependencies() -> None:

    node_modules: Path = FRONTEND_DIR / "node_modules"
    if node_modules.exists():
        logger.info("Dependencies already installed, skipping npm install")
        return
    run_command([NPM_CMD, "install"], cwd=FRONTEND_DIR)


def build_frontend() -> None:

    run_command([NPM_CMD, "run", "build"], cwd=FRONTEND_DIR)


def copy_dist_to_static() -> None:

    logger.info("Copying dist/* to static/")
    for item in DIST_DIR.iterdir():
        dest: Path = STATIC_DIR / item.name
        if item.is_dir():
            if dest.exists():
                for sub_item in item.rglob("*"):
                    target_path: Path = STATIC_DIR / sub_item.relative_to(DIST_DIR)
                    if sub_item.is_dir():
                        target_path.mkdir(parents=True, exist_ok=True)
                    else:
                        shutil.copy2(sub_item, target_path)
            else:
                shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
    logger.info("Copy finished!")


def build_react_frontend() -> None:

    install_dependencies()
    build_frontend()
    copy_dist_to_static()
    logger.info("Frontend build complete!")


if __name__ == "__main__":
    build_react_frontend()
