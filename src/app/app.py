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
from dash import Dash, html  # type: ignore

from .poincare.figure import build_poincare_figure
from .poincare.layout import build_layout

# Tentative d'import de la page Poincaré pour récupérer sa figure immuable
try:
    _pages_poincare = importlib.import_module("src.app.pages.poincare")
    _poincare_page_get_figure = getattr(_pages_poincare, "get_figure", None)
except Exception:
    _poincare_page_get_figure = None

__all__ = ["create_app", "app"]


def create_app() -> Dash:
    """Instancier l'application Dash (multipage natif)."""
    app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

    # Figure partagée (utilisée pour le fallback ou peut être régénérée dans une page auto-découverte)
    base_figure = build_poincare_figure()

    if dash.page_registry:
        # Pages auto‑découvertes présentes
        app.layout = html.Div(
            [
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
        # Les pages sont responsables d'attacher leurs propres callbacks (aucun appel ici).
    else:
        # Fallback: aucune page déclarée, on fournit directement la vue Poincaré (inclut IDs nécessaires).
        app.layout = build_layout(base_figure)
        # Dans ce mode sans pages découvertes, les callbacks ne sont pas attachés automatiquement.
        # Pour réactiver l'interactivité en mode fallback, réintroduire l'import et l'appel à register_callbacks.

    return app


# Instance prête à l'import (gunicorn, waitress, etc.)
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
