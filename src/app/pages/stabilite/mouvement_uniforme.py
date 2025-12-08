"""Page Stabilité – Mouvement uniforme: enregistre /stabilite/mouvement_uniforme et construit le layout descriptif."""

from __future__ import annotations

import dash
from dash import html

# from src.app.app import app  # removed to avoid circular import; use dash.get_app() instead
from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.mouvement_uniforme import layout_pedagogic
from src.app.stabilite.mouvement_uniforme import \
    register_callbacks as _register_callbacks

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/mouvement_uniforme.")

dash.register_page(
    __name__,
    path="/stabilite/mouvement_uniforme",
    name="Stabilité (mouvement uniforme)",
    title="Stabilité – Mouvement uniforme",
    order=16,
    description="Informations sur le cas 'mouvement uniforme' du diagramme de Poincaré (placeholder).",
)

log.debug("Construction du layout de la page mouvement uniforme...")

layout = build_stability_layout(
    "mouvement_uniforme", layout_pedagogic, tau=0.0, delta=0.0
)
_register_callbacks(dash.get_app())

log.info("Layout de la page mouvement uniforme construit.")
