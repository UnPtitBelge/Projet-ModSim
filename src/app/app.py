"""
Application Dash multipage native (use_pages) pour les visualisations.

Découverte automatique des pages via le dossier `pages/` (chaque fichier appelle dash.register_page).
Chaque page gère ses propres callbacks (principe de responsabilité locale).

Comportement:
- Pages détectées : barre de navigation + dash.page_container
- Aucune page détectée : fallback affichant directement le diagramme de Poincaré (sans interactivité par défaut)

Pour une page Poincaré auto‑découverte:
    src/app/pages/poincare.py
        import dash
        from dash import dcc, html
        from src.app.poincare.figure import build_poincare_figure
        from src.app.poincare.layout import build_layout
        from src.app.poincare.callbacks import register_callbacks
        dash.register_page(__name__, path="/", name="Poincaré", title="Diagramme de Poincaré")
        fig = build_poincare_figure()
        layout = build_layout(fig)
        register_callbacks(dash.get_app(), fig)  # attache les callbacks dans la page

Usage:
    python -m src.app.app
    ou: python Projet-ModSim/src/app/app.py
"""

from __future__ import annotations

import importlib

import dash
from dash import Dash, dcc, html  # type: ignore

from .logging_setup import get_logger, init_logging
from .poincare.figure import build_poincare_figure
from .poincare.layout import build_layout

# Initialisation centralisée du logging (idempotent)
_init_logging_cfg = init_logging()
log = get_logger(__name__)
# log.info("Initialisation de l'application Dash (multipage)")  # supprimé (silence console)
# log.info("Fichier de log actif: %s", _init_logging_cfg.file_path)  # supprimé

# Suppression de l'import prématuré de la page Poincaré.
# Dash découvrira automatiquement les pages après instanciation (use_pages=True).
_poincare_page_get_figure = None

__all__ = ["create_app", "app"]


def create_app() -> Dash:
    """Instancier l'application Dash (multipage natif)."""
    # log.debug("Création de l'instance Dash...")  # supprimé
    app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

    # Figure partagée (utilisée pour le fallback ou peut être régénérée dans une page auto-découverte)
    base_figure = build_poincare_figure()
    # log.debug("Figure Poincaré de base construite.")  # supprimé

    if dash.page_registry:
        log.debug(
            "Pages détectées (%d) : %s",
            len(dash.page_registry),
            [p["path"] for p in dash.page_registry.values()],
        )
        # Pages auto‑découvertes présentes
        app.layout = html.Div(
            [
                dcc.Location(id="url", refresh=True),
                html.Nav(
                    [
                        html.Span("Navigation:", style={"marginRight": "12px"}),
                        *[
                            html.A(
                                page["name"],
                                href=page["path"],
                                style={"marginRight": "16px"},
                            )
                            for page in sorted(
                                dash.page_registry.values(),
                                key=lambda p: p.get("order", 0),
                            )
                        ],
                    ],
                    style={
                        "padding": "10px 16px",
                        "backgroundColor": "#f5f5f5",
                        "borderBottom": "1px solid #ddd",
                        "marginBottom": "12px",
                    },
                ),
                dash.page_container,
            ]
        )
        # log.debug("Layout principal avec pages multipage configuré.")  # supprimé
        # Les pages sont responsables d'attacher leurs propres callbacks (aucun appel ici).
    else:
        # Fallback: aucune page déclarée, on fournit directement la vue Poincaré (inclut IDs nécessaires).
        log.warning("Aucune page détectée. Utilisation du layout fallback Poincaré.")
        app.layout = build_layout(base_figure)
        # Dans ce mode sans pages découvertes, les callbacks ne sont pas attachés automatiquement.
        # Pour réactiver l'interactivité en mode fallback, réintroduire l'import et l'appel à register_callbacks.

    # log.debug("Configuration du layout terminée, retour de l'application.")  # supprimé
    return app


# Instance prête à l'import (gunicorn, waitress, etc.)
app = create_app()
# log.info("Instance Dash créée et prête à l'import.")  # supprimé

if __name__ == "__main__":
    # log.info("Démarrage du serveur de développement Dash (debug=%s)", True)  # supprimé
    app.run(debug=True)
