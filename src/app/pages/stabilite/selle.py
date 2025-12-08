"""Page Stabilité – Selle: enregistre /stabilite/selle et construit le layout descriptif."""

import dash
from dash import dcc, html

# from src.app.app import app  # removed to avoid circular import; use dash.get_app() instead
from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.selle import layout_pedagogic
from src.app.stabilite.selle import register_callbacks as _register_callbacks

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/selle.")

dash.register_page(
    __name__,
    path="/stabilite/selle",
    name="Selle",
    title="Stabilité – Selle",
    order=14,
    description="Informations sur la selle du diagramme de Poincaré.",
)

log.debug("Construction du layout de la page selle...")

layout = build_stability_layout("selle", layout_pedagogic, tau=0.0, delta=-1.0)
_register_callbacks(dash.get_app())

log.info("Layout de la page selle construit.")
