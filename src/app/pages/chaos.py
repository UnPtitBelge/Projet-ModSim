"""
Page Chaos: enregistre /chaos et construit le layout avec palette inversée.
"""

from __future__ import annotations

import dash
from dash import html

from src.app.chaos import callbacks  # noqa: F401
from src.app.chaos.layout import build_layout
from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /chaos.")

dash.register_page(
    __name__,
    path="/chaos",
    name="Chaos",
    title="Chaos – Systèmes dynamiques non-linéaires",
    description="Exploration expérimentale des systèmes chaotiques et dynamiques non-linéaires.",
    order=3,
)

layout = build_layout()

log.info("Layout de la page /chaos construit.")
