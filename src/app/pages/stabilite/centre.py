"""Page Stabilité – Centre: enregistre /stabilite/centre et construit le layout descriptif."""

from __future__ import annotations

import dash

# removed unused dash imports
from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.centre import layout_pedagogic
from src.app.stabilite.centre import register_callbacks as _register_callbacks

# removed unused style component imports
# removed unused text style import

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/centre.")

dash.register_page(
    __name__,
    path="/stabilite/centre",
    name="Stabilité (centre)",
    title="Stabilité – Centre",
    order=15,
    description="Informations sur le cas 'centre' du diagramme de Poincaré (placeholder).",
)

log.debug("Construction du layout de la page centre...")

layout = build_stability_layout("centre", layout_pedagogic, tau=0.0, delta=1.0)

_register_callbacks(dash.get_app())

log.info("Layout de la page centre construit.")
