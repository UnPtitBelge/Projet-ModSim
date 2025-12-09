"""
Module principal pour la page d'analyse interactive de stabilité.

Fournit une interface interactive permettant d'explorer le comportement
des systèmes dynamiques linéaires 2D en fonction de leurs paramètres (τ, Δ).

Ce module réexporte les fonctions principales depuis le sous-package main_stability.
"""

from __future__ import annotations

from dash import Dash, html

from .main_stability import build_layout, get_ids, register_callbacks

__all__ = ["get_ids", "build_layout", "register_callbacks"]
