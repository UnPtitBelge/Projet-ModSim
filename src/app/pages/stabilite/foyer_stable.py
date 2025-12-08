"""Page Stabilité – Foyer stable: enregistre /stabilite/foyer_stable et construit le layout descriptif."""

import dash
from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.foyer_stable import layout_pedagogic
from src.app.stabilite.foyer_stable import \
    register_callbacks as _register_callbacks

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/foyer_stable.")

dash.register_page(
    __name__,
    path="/stabilite/foyer_stable",
    name="Foyer stable",
    title="Stabilité – Foyer stable",
    order=10,
    description="Informations sur le foyer stable du diagramme de Poincaré.",
)

log.debug("Construction du layout de la page foyer stable...")
layout = build_stability_layout("foyer_stable", layout_pedagogic, tau=-2.0, delta=2.0)
_register_callbacks(dash.get_app())

log.info("Layout de la page foyer stable construit.")
