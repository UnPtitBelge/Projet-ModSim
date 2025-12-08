from __future__ import annotations

import dash
from dash import Dash, dcc, html  # type: ignore

from .logging_setup import get_logger, init_logging
from .poincare.figure import build_poincare_figure
from .poincare.layout import build_layout
from .style.components.layout import content_wrapper
from .style.components.sidebar import (nav_link, sidebar_container,
                                       sidebar_header)

_init_logging_cfg = init_logging()
log = get_logger(__name__)


_poincare_page_get_figure = None

__all__ = ["create_app", "app"]


def create_app() -> Dash:
    """Instancier l'application Dash."""

    app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
    app.index_string = """<!DOCTYPE html>
<html>
  <head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <script>
      window.MathJax = {
        tex: {
          inlineMath: [['$', '$']],
          displayMath: [['$$', '$$']],
          processEscapes: true,
          packages: {'[+]': ['ams']},
          tags: 'ams'
        },
        options: {
          skipHtmlTags: ['script', 'noscript', 'style', 'textarea'],
          ignoreHtmlClass: 'tex2jax_ignore',
          processHtmlClass: 'tex2jax_process'
        },
        chtml: {
          fontURL: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2',
          scale: 1.0
        }
      };
    </script>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
    <style>
      mjx-container[jax="CHTML"][display="inline"] { display: inline !important; }
      mjx-container[jax="CHTML"][display="true"] {
        display: block !important;
        text-align: center;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        padding: 0.25rem 0;
      }
      a mjx-container, button mjx-container { font-size: 0.95em; }
    </style>
  </head>
  <body>
    {%app_entry%}
    <footer>
      {%config%}
      {%scripts%}
      {%renderer%}
    </footer>
    <script>
      (function() {
        function typeset() {
          if (window.MathJax && MathJax.typesetPromise) {
            MathJax.typesetPromise();
          }
        }
        if (document.readyState === 'complete') {
          typeset();
        } else {
          window.addEventListener('load', typeset);
        }
        var appRoot = document.getElementById('_dash-app') || document.body;
        var observer = new MutationObserver(function() {
          clearTimeout(observer._mjxTimer);
          observer._mjxTimer = setTimeout(typeset, 50);
        });
        observer.observe(appRoot, { childList: true, subtree: true });
      })();
    </script>
  </body>
</html>"""

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
                                *[
                                    html.A(
                                        page["name"],
                                        href=page["path"],
                                        style=nav_link(),
                                    )
                                    for page in sorted(
                                        [
                                            p
                                            for p in dash.page_registry.values()
                                            if (
                                                not p.get("path", "").startswith(
                                                    "/stabilite"
                                                )
                                            )
                                            and (p.get("path", "") != "/about")
                                        ],
                                        key=lambda p: p.get("order", 0),
                                    )
                                ],
                                html.Details(
                                    [
                                        html.Summary(
                                            "Stabilité",
                                            style={
                                                "cursor": "pointer",
                                                "fontStyle": "normal",
                                                "padding": "8px 10px",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                *[
                                                    html.A(
                                                        subpage["name"],
                                                        href=subpage["path"],
                                                        style=nav_link(),
                                                    )
                                                    for subpage in sorted(
                                                        [
                                                            p
                                                            for p in dash.page_registry.values()
                                                            if p.get(
                                                                "path", ""
                                                            ).startswith("/stabilite")
                                                        ],
                                                        key=lambda p: p.get("order", 0),
                                                    )
                                                ]
                                            ],
                                            style={"marginTop": "6px"},
                                        ),
                                    ],
                                    open=True,
                                    style={},
                                ),
                                html.A(
                                    "À propos",
                                    href="/about",
                                    style=nav_link(),
                                ),
                            ],
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

    else:
        log.warning("Aucune page détectée. Utilisation du layout fallback Poincaré.")
        app.layout = build_layout(base_figure)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
