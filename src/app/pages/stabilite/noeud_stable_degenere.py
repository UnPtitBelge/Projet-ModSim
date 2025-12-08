"""Page Stabilité – Nœud stable dégénéré: enregistre /stabilite/noeud_stable_degenere et construit le layout descriptif."""

from __future__ import annotations

import dash
from dash import html

# from src.app.app import app  # removed to avoid circular import; use dash.get_app() instead
from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.noeud_stable_degenere import layout_pedagogic
from src.app.stabilite.noeud_stable_degenere import \
    register_callbacks as _register_callbacks

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/noeud_stable_degenere.")

dash.register_page(
    __name__,
    path="/stabilite/noeud_stable_degenere",
    name="Nœud stable dégénéré",
    title="Stabilité – Nœud stable dégénéré",
    order=17,
    description="Informations sur le cas 'nœud stable dégénéré' du diagramme de Poincaré (placeholder).",
)

log.debug("Construction du layout de la page noeud stable dégénéré...")

layout = build_stability_layout(
    "noeud_stable_degenere", layout_pedagogic, tau=-2.0, delta=1.0
)
_register_callbacks(dash.get_app())

log.info("Layout de la page noeud stable dégénéré construit.")
