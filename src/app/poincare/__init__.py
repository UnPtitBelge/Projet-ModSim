"""
Poincaré diagram subpackage.

Building blocks:
- build_poincare_figure / PoincareConfig
- register_callbacks (interactivity)
- build_layout (Dash layout)
- constants (bounds, colors, labels)
- zones (geometry helpers)

Quick start:
    from src.app.poincare import build_poincare_figure
    fig = build_poincare_figure()

The runnable Dash entry point lives in src/app/app.py.
"""

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
