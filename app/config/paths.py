from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths

EXECUTABLE_PATH = (
    Path(os.environ["APPIMAGE"]) if "APPIMAGE" in os.environ
    else Path(sys.argv[0]).resolve() if "__compiled__" in globals()
    else Path(sys.executable).resolve()
)

EXECUTABLE_DIR = (
    Path(sys.executable).resolve().parent
    if "__compiled__" in globals()
    else Path(".")
)

PORTABLE_DIR = EXECUTABLE_DIR / "幽灵下载者"
USER_DATA_DIR = Path(QStandardPaths.writableLocation(
    QStandardPaths.StandardLocation.GenericDataLocation
)) / "幽灵下载者"


def canWriteFolder(folder: Path) -> bool:
    """程序位于只读位置（Program Files、AppImage 挂载点）时无法写入，必须回落。"""
    try:
        folder.mkdir(parents=True, exist_ok=True)
        probe = folder / ".write_probe"
        probe.touch()
        probe.unlink()
        return True
    except OSError:
        return False


APP_DATA_DIR = PORTABLE_DIR if canWriteFolder(PORTABLE_DIR) else USER_DATA_DIR

SEED_FEATURES_DIR = EXECUTABLE_DIR / "features"
FEATURES_DIR = (
    SEED_FEATURES_DIR
    if "__compiled__" not in globals()
    else APP_DATA_DIR / "features"
)

DOWNLOAD_DIR = Path(QStandardPaths.writableLocation(
    QStandardPaths.StandardLocation.DownloadLocation
))


def isPortable() -> bool:
    return APP_DATA_DIR == PORTABLE_DIR


def migrate(target: Path) -> None:
    from loguru import logger
    logger.remove()
    source = APP_DATA_DIR
    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, dirs_exist_ok=True)
    if isPortable():
        source.rename(source.with_suffix(".bak"))
