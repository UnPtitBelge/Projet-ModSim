"""
Simplified logging setup for the Projet-ModSim application.

Goals:
- No environment variables.
- Always log to a dedicated file: <project_root>/logs/app.log
- Console output kept minimal (WARNING and above).
- File log retains informative detail (INFO and above).
- Idempotent initialization (safe to call multiple times).
- Rotating file to avoid uncontrolled growth.

Usage:
    from src.app.logging_setup import init_logging, get_logger
    init_logging()  # do this once early (e.g., in app.py)
    log = get_logger(__name__)
    log.info("Application started")

Customization:
You can optionally pass parameters to init_logging(file_level=..., console_level=..., file_path=...)
if you need different verbosity or a custom path.

Log Levels:
- File handler: INFO (default) → keeps operational trace.
- Console handler: WARNING (default) → only crucial events (warnings, errors, critical).

Rotation:
- Max file size: 1,000,000 bytes
- Backup count: 5 (app.log.1 .. app.log.5)

Thread-safety:
A lock ensures only one initialization sequence runs even under concurrency.

Reconfiguration:
Call reconfigure_logging(...) to change levels or path at runtime.

"""

from __future__ import annotations

import logging
import os
import threading
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

__all__ = [
    "LoggingConfig",
    "init_logging",
    "get_logger",
    "reconfigure_logging",
    "is_logging_initialized",
]

# Internal state
_LOCK = threading.Lock()
_INITIALIZED = False
_ACTIVE_CONFIG: Optional["LoggingConfig"] = None


@dataclass(frozen=True)
class LoggingConfig:
    file_path: str
    file_level: int = logging.INFO
    console_level: int = logging.WARNING
    max_bytes: int = 1_000_000
    backup_count: int = 5
    file_fmt: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    console_fmt: str = "%(levelname)s | %(message)s"
    datefmt: str = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def default(file_path: Optional[str] = None) -> "LoggingConfig":
        if file_path is None:
            # Resolve project root: this file is at src/app/logging_setup.py
            project_root = Path(__file__).resolve().parents[2]
            logs_dir = project_root / "logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
            file_path = str(logs_dir / "app.log")
        return LoggingConfig(file_path=file_path)


def _build_file_handler(cfg: LoggingConfig) -> RotatingFileHandler:
    os.makedirs(os.path.dirname(cfg.file_path), exist_ok=True)
    handler = RotatingFileHandler(
        cfg.file_path,
        maxBytes=cfg.max_bytes,
        backupCount=cfg.backup_count,
        encoding="utf-8",
    )
    handler.setLevel(cfg.file_level)
    handler.setFormatter(logging.Formatter(cfg.file_fmt, cfg.datefmt))
    return handler


def _build_console_handler(cfg: LoggingConfig) -> logging.Handler:
    ch = logging.StreamHandler()
    ch.setLevel(cfg.console_level)
    ch.setFormatter(logging.Formatter(cfg.console_fmt, cfg.datefmt))
    return ch


def _apply_config(cfg: LoggingConfig) -> None:
    root = logging.getLogger()
    root.setLevel(min(cfg.file_level, cfg.console_level))  # base threshold

    # Remove current handlers (reconfiguration scenario)
    for h in list(root.handlers):
        root.removeHandler(h)

    # File handler (informational detail)
    fh = _build_file_handler(cfg)
    root.addHandler(fh)

    # Console handler (minimal noise)
    ch = _build_console_handler(cfg)
    root.addHandler(ch)

    # Reduce verbosity of third-party libraries
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("plotly").setLevel(logging.WARNING)

    # Confirmation (only to file, not to console unless level permits)
    root.debug(
        "Logging configured (file=%s, file_level=%s, console_level=%s)",
        cfg.file_path,
        logging.getLevelName(cfg.file_level),
        logging.getLevelName(cfg.console_level),
    )


def init_logging(
    file_path: Optional[str] = None,
    file_level: int = logging.INFO,
    console_level: int = logging.WARNING,
    force: bool = False,
) -> LoggingConfig:
    """
    Initialize logging (idempotent).
    If force=True, previous configuration is overridden.
    """
    global _INITIALIZED, _ACTIVE_CONFIG
    with _LOCK:
        if _INITIALIZED and not force and _ACTIVE_CONFIG:
            return _ACTIVE_CONFIG

        cfg = LoggingConfig.default(file_path)
        cfg = LoggingConfig(
            file_path=cfg.file_path,
            file_level=file_level,
            console_level=console_level,
            max_bytes=cfg.max_bytes,
            backup_count=cfg.backup_count,
            file_fmt=cfg.file_fmt,
            console_fmt=cfg.console_fmt,
            datefmt=cfg.datefmt,
        )
        _apply_config(cfg)
        _INITIALIZED = True
        _ACTIVE_CONFIG = cfg
        logging.getLogger(__name__).info(
            "File logging active at %s (file_level=%s, console_level=%s)",
            cfg.file_path,
            logging.getLevelName(cfg.file_level),
            logging.getLevelName(cfg.console_level),
        )
        return cfg


def reconfigure_logging(
    file_path: Optional[str] = None,
    file_level: Optional[int] = None,
    console_level: Optional[int] = None,
) -> LoggingConfig:
    """
    Reconfigure logging at runtime.
    Example:
        reconfigure_logging(console_level=logging.ERROR)
    """
    base = _ACTIVE_CONFIG or LoggingConfig.default()
    new_cfg = LoggingConfig(
        file_path=file_path or base.file_path,
        file_level=file_level or base.file_level,
        console_level=console_level or base.console_level,
        max_bytes=base.max_bytes,
        backup_count=base.backup_count,
        file_fmt=base.file_fmt,
        console_fmt=base.console_fmt,
        datefmt=base.datefmt,
    )
    return init_logging(
        file_path=new_cfg.file_path,
        file_level=new_cfg.file_level,
        console_level=new_cfg.console_level,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Obtain a logger for the given module/package name.
    Ensures logging is initialized.
    """
    if not _INITIALIZED:
        init_logging()
    return logging.getLogger(name)


def is_logging_initialized() -> bool:
    return _INITIALIZED


# Auto-init (can be commented out if explicit control desired)
if not _INITIALIZED:
    init_logging()
