"""
Rich API for the Poincaré diagram.

Provides:
- create_app() / get_app() for the Dash application
- build_poincare_figure(), PoincareConfig
- register_callbacks

Lazy import of app.py avoids runpy warnings and keeps the package extensible
for future visualizations (e.g. phase, bifurcation).
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

from .poincare.callbacks import register_callbacks
# Re-export figure construction and callbacks directly (these are pure modules).
from .poincare.figure import PoincareConfig, build_poincare_figure

__version__ = "0.1.1"

__all__ = [
    "create_app",
    "get_app",
    "build_poincare_figure",
    "PoincareConfig",
    "register_callbacks",
    "__version__",
]


def _load_app_module():
    """
    Internal helper: lazily import the launcher module.

    Using import_module instead of a direct relative import avoids importing
    `src.app.app` during package initialization, preventing runpy warnings.
    """
    # __name__ == 'src.app' here, so f"{__name__}.app" -> 'src.app.app'
    return import_module(f"{__name__}.app")


def create_app() -> Any:
    """
    Return a freshly constructed Dash application by delegating
    to `create_app` defined in `app.py`.
    """
    mod = _load_app_module()
    return mod.create_app()


def get_app() -> Any:
    """
    Return the singleton Dash application instance defined as `app`
    in `app.py`. Import is performed lazily.
    """
    mod = _load_app_module()
    return mod.app
