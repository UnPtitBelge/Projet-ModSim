from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, dcc, html  # type: ignore

from .logging_setup import get_logger, init_logging
from .poincare.figure import build_poincare_figure
from .poincare.layout import build_layout
from .style.components.layout import content_wrapper
from .style.components.sidebar import (chaos_badge, nav_link, other_badge,
                                       poincare_badge, sidebar_container,
                                       sidebar_header, stabilite_badge)
from .style.html_head import get_index_string

_init_logging_cfg = init_logging()
log = get_logger(__name__)


_poincare_page_get_figure = None

__all__ = ["create_app", "app"]


def create_app() -> Dash:
    """Instancier l'application Dash."""

    app = Dash(
        __name__,
        use_pages=True,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )
    app.index_string = get_index_string()

    base_figure = build_poincare_figure()

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
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Menu",
                                    style=sidebar_header(),
                                ),
                                # Home page
                                html.A(
                                    "Accueil",
                                    href="/",
                                    style=other_badge(),
                                ),
                                # Poincaré badge
                                html.A(
                                    "Poincaré",
                                    href="/poincare",
                                    style=poincare_badge(),
                                    title="Explorer le diagramme de Poincaré et les points d'équilibre associés",
                                ),
                                # Stabilité badge
                                html.A(
                                    "Stabilité",
                                    href="/stabilite",
                                    style=stabilite_badge(),
                                    title="Analyser la stabilité des systèmes linéaires d'ordre 2",
                                ),
                                # Chaos badge
                                html.A(
                                    "Chaos",
                                    href="/chaos",
                                    style=chaos_badge(),
                                    title="Explore chaotic systems and non-linear dynamics",
                                ),
                                # About page (On the bottom)
                                html.Div(
                                    [
                                        html.A(
                                            "À propos",
                                            href="/about",
                                            style=other_badge(),
                                        ),
                                    ],
                                    style={"marginTop": "auto"},
                                ),
                            ],
                            id="sidebar-container",
                            style=sidebar_container(),
                        ),
                        html.Div(
                            [
                                dash.page_container,
                            ],
                            style=content_wrapper(),
                        ),
                    ]
                ),
            ]
        )

        # Callback to invert sidebar colors on chaos page
        @app.callback(
            Output("sidebar-container", "className"),
            Input("url", "pathname"),
        )
        def update_sidebar_colors(pathname: str) -> str:
            """Update sidebar styling based on current page."""
            if pathname == "/chaos":
                return "chaos-mode"
            return ""

    else:
        log.warning("Aucune page détectée. Utilisation du layout fallback Poincaré.")
        app.layout = build_layout(base_figure)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
