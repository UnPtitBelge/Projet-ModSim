"""Poincaré subpackage: re-exports figure building, layout, callbacks, constants, and zones."""

from __future__ import annotations

from . import constants, zones
from .callbacks import register_callbacks
from .figure import PoincareConfig, build_poincare_figure
from .layout import build_layout

__all__ = [
    "build_poincare_figure",
    "PoincareConfig",
    "register_callbacks",
    "build_layout",
    "constants",
    "zones",
]

__version__ = "0.1.0"
