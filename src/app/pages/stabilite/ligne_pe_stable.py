"""Page Stabilité – Ligne de points d’équilibre stable: enregistre /stabilite/ligne_pe_stable et construit le layout descriptif."""

from __future__ import annotations

import dash
from dash import dcc, html

# from src.app.app import app  # removed to avoid circular import; use dash.get_app() instead
from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.ligne_pe_stable import layout_pedagogic
from src.app.stabilite.ligne_pe_stable import \
    register_callbacks as _register_callbacks
from src.app.style.components.layout import app_container, page_text_container
from src.app.style.text import TEXT

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/ligne_pe_stable.")

dash.register_page(
    __name__,
    path="/stabilite/ligne_pe_stable",
    name="Ligne de PE stable",
    title="Stabilité – Ligne de points d’équilibre stable",
    order=19,
    description="Informations sur la ligne de points d’équilibre stable (placeholder).",
)

log.debug("Construction du layout de la page ligne de points d'équilibre stable...")

layout = build_stability_layout(
    "ligne_pe_stable", layout_pedagogic, tau=-1.0, delta=0.0
)
_register_callbacks(dash.get_app())

log.info("Layout de la page ligne de points d'equilibre stable construit.")
