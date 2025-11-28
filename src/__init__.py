"""Racine du package src (ModSim).

Rend le package importable et offre des raccourcis:
- from src import create_app, get_app

Import paresseux pour éviter le coût et les effets secondaires lors de
l'importation de `src` (construction de la figure, configuration Dash, logging).
"""

from importlib import import_module
from typing import Any

__all__ = ["create_app", "get_app", "__version__"]
__version__ = "0.1.1"


def _load_app_module():
    """
    Importer paresseusement le sous-module principal `src.app`.
    Séparé pour lisibilité et éventuelle extension future.
    """
    return import_module("src.app")


def create_app() -> Any:
    """
    Fabrique une nouvelle instance de l'application Dash.
    Permet `from src import create_app`.
    """
    mod = _load_app_module()
    return mod.create_app()


def get_app() -> Any:
    """
    Retourne l'instance singleton de l'application Dash définie dans `src.app.app`.
    """
    mod = _load_app_module()
    return getattr(mod, "app", None)
