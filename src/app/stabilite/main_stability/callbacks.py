"""
Callbacks pour la page principale de stabilité.
"""

import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, html
from scipy.integrate import odeint

from src.app.style.text import TEXT

from ..base_figures import create_phase_diagram, create_system_graph
from ..eigenvalue_utils import (
    classify_equilibrium,
    format_eigenvalue_display,
    tau_delta_to_matrix,
)
from .constants import get_ids


def register_callbacks(app: Dash) -> None:
    """
    Enregistre tous les callbacks pour la page interactive.

    Args:
        app: Application Dash
    """
    ids = get_ids()

    # Affichage du type d'équilibre
    @app.callback(
        Output(ids["equilibrium_type"], "children"),
        [Input(ids["tau_slider"], "value"), Input(ids["delta_slider"], "value")],
    )
    def display_equilibrium_type(tau, delta):
        """Affiche le type d'équilibre basé sur τ et Δ."""
        eq_type = classify_equilibrium(tau, delta)
        return eq_type

    # Affichage de l'EDO
    @app.callback(
        Output(ids["ode_display"], "children"),
        [Input(ids["tau_slider"], "value"), Input(ids["delta_slider"], "value")],
    )
    def display_ode(tau, delta):
        """Affiche les équations différentielles du système."""
        a, b, c, d = tau_delta_to_matrix(tau, delta)

        # Construction des termes pour x₁
        x1_terms = []
        if abs(a) > 1e-10:
            x1_terms.append(f"{a:.2f} x_1")
        if abs(b) > 1e-10:
            x1_terms.append(f"{b:.2f} x_2" if b > 0 else f"- {abs(b):.2f} x_2")
        x1_expr = " + ".join(x1_terms) if x1_terms else "0"

        # Construction des termes pour x₂
        x2_terms = []
        if abs(c) > 1e-10:
            x2_terms.append(f"{c:.2f} x_1")
        if abs(d) > 1e-10:
            x2_terms.append(f"{d:.2f} x_2" if d > 0 else f"- {abs(d):.2f} x_2")
        x2_expr = " + ".join(x2_terms) if x2_terms else "0"

        # Nettoyage des expressions
        x1_expr = x1_expr.replace("+ -", "- ")
        x2_expr = x2_expr.replace("+ -", "- ")

        return html.Div(
            [
                html.Div(f"$$\\dot{{x}}_1 = {x1_expr}$$", className="tex2jax_process"),
                html.Div(f"$$\\dot{{x}}_2 = {x2_expr}$$", className="tex2jax_process"),
            ]
        )

    # Affichage des valeurs propres
    @app.callback(
        Output(ids["eigenvalue_display"], "children"),
        [Input(ids["tau_slider"], "value"), Input(ids["delta_slider"], "value")],
    )
    def display_eigenvalues(tau, delta):
        """Affiche les valeurs propres et leur nature."""
        eigenvalue_info = format_eigenvalue_display(tau, delta)

        return html.Div(
            [
                html.P(
                    [
                        html.Strong("Valeurs propres : "),
                        eigenvalue_info["eigenvalues"],
                    ],
                    style={**TEXT["p"], "margin": "4px 0"},
                ),
                html.P(
                    [
                        html.Strong("Nature : "),
                        eigenvalue_info["nature"],
                    ],
                    style={**TEXT["p"], "margin": "4px 0"},
                ),
            ]
        )

    # Génération du graphique temporel
    @app.callback(
        Output(ids["system_graph"], "figure"),
        [Input(ids["tau_slider"], "value"), Input(ids["delta_slider"], "value")],
    )
    def update_system_graph(tau, delta):
        """Génère le graphique d'évolution temporelle x₁(t) et x₂(t)."""
        a, b, c, d = tau_delta_to_matrix(tau, delta)
        initial_condition = (1.0, 0.5)
        title = "Évolution temporelle du système"

        return create_system_graph(a, b, c, d, initial_condition, title)

    # Génération du diagramme de phase (statique)
    @app.callback(
        Output(ids["phase_diagram"], "figure"),
        [
            Input(ids["tau_slider"], "value"),
            Input(ids["delta_slider"], "value"),
        ],
    )
    def update_phase_diagram(tau, delta):
        """Génère le diagramme de phase (sans animation)."""
        a, b, c, d = tau_delta_to_matrix(tau, delta)
        title = "Portrait de phase"
        return create_phase_diagram(a, b, c, d, title)

