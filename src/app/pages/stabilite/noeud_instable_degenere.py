"""Page Stabilité – Nœud instable dégénéré: enregistre /stabilite/noeud_instable_degenere et construit le layout descriptif."""

from __future__ import annotations

import dash
from dash import html

# from src.app.app import app  # removed to avoid circular import; use dash.get_app() instead
from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.noeud_instable_degenere import layout_pedagogic
from src.app.stabilite.noeud_instable_degenere import \
    register_callbacks as _register_callbacks
from src.app.style.components.layout import app_container, page_text_container
from src.app.style.text import TEXT

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/noeud_instable_degenere.")

dash.register_page(
    __name__,
    path="/stabilite/noeud_instable_degenere",
    name="Nœud instable dégénéré",
    title="Stabilité – Nœud instable dégénéré",
    order=18,
    description="Informations sur le cas 'nœud instable dégénéré' du diagramme de Poincaré (placeholder).",
)

log.debug("Construction du layout de la page noeud instable dégénéré...")

layout = build_stability_layout(
    "noeud_instable_degenere", layout_pedagogic, tau=2.0, delta=1.0
)
_register_callbacks(dash.get_app())

log.info("Layout de la page noeud instable dégénéré construit.")
