"""
Module main_stability pour la page d'analyse interactive de stabilité.

Ce module organise la page principale de stabilité en plusieurs sous-modules :
- constants : identifiants des composants
- layout : construction de l'interface utilisateur
- callbacks : logique interactive
- plots : fonctions de génération de graphiques (si nécessaire)
"""

from .callbacks import register_callbacks
from .constants import get_ids
from .layout import build_layout

__all__ = ["get_ids", "build_layout", "register_callbacks"]
