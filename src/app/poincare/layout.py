from dash import dcc, html


def build_layout(figure):
    """Return the main layout (title, graph, info panels) for the Poincaré diagram."""
    return html.Div(
        [
            html.H2(
                "Analyse et découverte de la notion de stabilité pour des systèmes linéaires continus d'ordre deux"
            ),
            dcc.Graph(
                id="poincaré-graph",
                figure=figure,
                style={"height": "70vh"},
                config={
                    "displaylogo": False,
                    "modeBarButtonsToRemove": [
                        "toImage",
                        "lasso2d",
                        "select2d",
                        "autoScale2d",
                    ],
                },
            ),
            html.Div(
                [
                    html.P(
                        (
                            "Ce diagramme de Poincaré illustre différentes zones liées à la stabilité locale "
                            "des systèmes linéaires du second ordre en fonction des paramètres Tau (τ) et Delta (Δ). "
                            "La parabole noire sépare les régions supérieures et inférieures. "
                            "Survolez ou cliquez sur une zone pour la mettre en évidence."
                        )
                    ),
                    html.Div(id="output-temp-hover", style={"marginTop": "14px"}),
                    html.Div(id="output-temp-click", style={"marginTop": "8px"}),
                ],
                style={
                    "maxWidth": "860px",
                    "fontSize": "0.95rem",
                    "lineHeight": "1.35",
                },
            ),
        ],
        style={
            "padding": "20px",
            "fontFamily": "Arial, sans-serif",
        },
    )


__all__ = ["build_layout"]
