"""
Page principale d'analyse interactive de stabilité.

Cette page permet d'explorer interactivement le comportement des systèmes
dynamiques linéaires 2D en ajustant les paramètres τ (trace) et Δ (déterminant).
"""

from __future__ import annotations

import dash

from src.app.logging_setup import get_logger
from src.app.stabilite.main_stabilite_page import (build_layout,
                                                   register_callbacks)

log = get_logger(__name__)
log.info("Enregistrement de la page principale /stabilite.")

dash.register_page(
    __name__,
    path="/stabilite",
    name="Analyse de stabilité",
    title="Analyse de stabilité – Systèmes linéaires",
    description="Analyse interactive de la stabilité des systèmes dynamiques linéaires d'ordre 2.",
    order=2,
)

# Construction du layout
layout = build_layout()

# Enregistrement des callbacks
register_callbacks(dash.get_app())

log.info("Layout de la page /stabilite construit.")
