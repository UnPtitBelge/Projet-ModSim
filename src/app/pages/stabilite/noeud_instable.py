"""Page Stabilité – Nœud instable: enregistre /stabilite/noeud_instable et construit le layout descriptif."""

import dash
from dash import html

# from src.app.app import app  # removed to avoid circular import; use dash.get_app() instead
from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.noeud_instable.layout import (
    register_callbacks as _register_callbacks,
)

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/noeud_instable.")

dash.register_page(
    __name__,
    path="/stabilite/noeud_instable",
    name="Stabilité (nœud instable)",
    title="Stabilité – Nœud instable",
    order=13,
    description="Informations sur le nœud instable du diagramme de Poincaré.",
)

log.debug("Construction du layout de la page nœud instable...")

layout = build_stability_layout("noeud_instable")
_register_callbacks(dash.get_app())

log.info("Layout de la page nœud instable construit.")
