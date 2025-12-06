"""Page Stabilité – Nœud stable: enregistre /stabilite/noeud_stable et construit le layout descriptif."""

import dash
from dash import dcc, html

# from src.app.app import app  # removed to avoid circular import; use dash.get_app() instead
from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.noeud_stable.layout import (
    register_callbacks as _register_callbacks,
)

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/noeud_stable.")

dash.register_page(
    __name__,
    path="/stabilite/noeud_stable",
    name="Stabilité (nœud stable)",
    title="Stabilité – Nœud stable",
    order=12,
    description="Informations sur le nœud stable du diagramme de Poincaré.",
)

log.debug("Construction du layout de la page noeud stable...")
layout = build_stability_layout("noeud_stable")
_register_callbacks(dash.get_app())

log.info("Layout de la page noeud stable construit.")
