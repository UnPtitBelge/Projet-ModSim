"""
Callbacks Dash pour la page du problème à trois corps.

Gère les interactions utilisateur et la génération dynamique des simulations.
"""

from dash import Input, Output, State, callback, ctx, html

from src.app.chaos.plots import build_three_body_figure_with_data


@callback(
    Output("chaos-three-body-graph", "figure"),
    Output("chaos-initial-conditions", "children"),
    Input("chaos-restart-button", "n_clicks"),
    Input("chaos-reset-button", "n_clicks"),
    prevent_initial_call=False,
)
def update_three_body_figure(restart_n_clicks, reset_n_clicks):
    """
    Génère une nouvelle simulation avec ou sans perturbations aléatoires.
    
    Deux comportements possibles:
    - Bouton "Générer": positions aléatoires avec perturbations
    - Bouton "Reset": retour à la configuration de base sans perturbations
    
    Args:
        restart_n_clicks: Nombre de clics sur "Générer"
        reset_n_clicks: Nombre de clics sur "Reset"
    
    Returns:
        fig: Figure Plotly avec la nouvelle animation
        conditions_text: Composant HTML affichant les positions initiales
    """
    # Déterminer quel bouton a déclenché le callback
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        randomize = button_id == "chaos-restart-button"
    else:
        # Chargement initial
        randomize = False
    
    fig, bodies, _, _ = build_three_body_figure_with_data(randomize=randomize)
    
    # Créer l'affichage des conditions initiales avec couleurs
    conditions_text = html.Div(
        [
            html.H5(
                "Positions initiales :",
                style={"marginTop": "10px", "marginBottom": "10px"},
            ),
            html.Ul(
                [
                    html.Li(
                        [
                            html.Span(
                                "●",
                                style={
                                    "color": body.color,
                                    "marginRight": "8px",
                                    "fontSize": "16px",
                                },
                            ),
                            html.Span(
                                f"{body.name}: ",
                                style={"fontWeight": "600", "color": body.color},
                            ),
                            f"x={body.position[0]:.6f}, y={body.position[1]:.6f}",
                        ]
                    )
                    for body in bodies
                ],
                style={
                    "fontSize": "12px",
                    "fontFamily": "monospace",
                    "lineHeight": "1.6",
                    "listStyleType": "none",
                    "paddingLeft": "0",
                },
            ),
        ],
        style={
            "backgroundColor": "#f5f5f5",
            "padding": "10px",
            "borderRadius": "4px",
            "marginTop": "10px",
        },
    )
    
    return fig, conditions_text
