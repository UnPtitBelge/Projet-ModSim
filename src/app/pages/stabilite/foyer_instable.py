"""Page Stabilité – Foyer instable: enregistre /stabilite/foyer_instable et construit le layout descriptif."""

import dash
from dash import dcc, html

# from src.app.app import app  # removed to avoid circular import; use dash.get_app() instead
from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.foyer_instable.layout import (
    register_callbacks as _register_callbacks,
)

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/foyer_instable.")

dash.register_page(
    __name__,
    path="/stabilite/foyer_instable",
    name="Stabilite (foyer instable)",
    title="Stabilite – Foyer instable",
    order=11,
    description="Informations sur le foyer instable du diagramme de Poincaré.",
)
log.debug("Construction du layout de la page foyer instable...")
layout = build_stability_layout("foyer_instable")
_register_callbacks(dash.get_app())

# layout is provided by build_stability_layout("foyer_instable")
# (ancien layout supprimé — layout fourni par build_stability_layout("foyer_instable"))
log.info("Layout de la page foyer instable construit.")
