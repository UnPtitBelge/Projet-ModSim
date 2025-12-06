"""Page Stabilité – Ligne de PE instable: enregistre /stabilite/ligne_pe_instable et construit le layout descriptif."""

from __future__ import annotations

import dash
from dash import dcc, html

# from src.app.app import app  # removed to avoid circular import; use dash.get_app() instead
from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.ligne_pe_instable.layout import (
    register_callbacks as _register_callbacks,
)
from src.app.style.components.layout import app_container, page_text_container
from src.app.style.text import TEXT

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/ligne_pe_instable.")

dash.register_page(
    __name__,
    path="/stabilite/ligne_pe_instable",
    name="Stabilité (ligne de PE instable)",
    title="Stabilité – Ligne de points d’équilibre instable",
    order=20,
    description="Informations sur la ligne de points d’équilibre instable (placeholder).",
)

log.debug("Construction du layout de la page ligne de points d’équilibre instable...")

layout = build_stability_layout("ligne_pe_instable")
_register_callbacks(dash.get_app())

log.info("Layout de la page ligne de points d’équilibre instable construit.")
