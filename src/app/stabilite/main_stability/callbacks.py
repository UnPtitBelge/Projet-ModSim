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

    # Génération du diagramme de phase avec point cliqué
    @app.callback(
        Output(ids["phase_diagram"], "figure"),
        [
            Input(ids["tau_slider"], "value"),
            Input(ids["delta_slider"], "value"),
            Input(ids["system_graph"], "clickData"),
        ],
        [State(ids["trajectory_store"], "data")],
    )
    def update_phase_diagram(tau, delta, click_data, trajectory_data):
        """Génère le diagramme de phase avec un marqueur au point cliqué."""
        a, b, c, d = tau_delta_to_matrix(tau, delta)
        title = "Portrait de phase"

        fig = create_phase_diagram(a, b, c, d, title)

        # Si on a des données de clic et de trajectoire, ajouter le marqueur
        if click_data and trajectory_data:
            try:
                # Récupérer le temps cliqué
                t_clicked = click_data["points"][0]["x"]
                
                # Récupérer les données de trajectoire
                t_array = np.array(trajectory_data["t"])
                x1_array = np.array(trajectory_data["x1"])
                x2_array = np.array(trajectory_data["x2"])
                
                # Trouver l'index le plus proche du temps cliqué
                idx = np.argmin(np.abs(t_array - t_clicked))
                x1_point = x1_array[idx]
                x2_point = x2_array[idx]
                
                # Ajouter un marqueur au point (x1, x2)
                fig.add_trace(
                    go.Scatter(
                        x=[x1_point],
                        y=[x2_point],
                        mode="markers",
                        marker=dict(size=12, color="#10B981", symbol="circle", line=dict(width=2, color="white")),
                        name=f"Point à t={t_clicked:.2f}",
                        hoverinfo="text",
                        hovertext=f"t={t_clicked:.2f}<br>x₁={x1_point:.3f}<br>x₂={x2_point:.3f}",
                        showlegend=True,
                    )
                )
            except (KeyError, IndexError, TypeError):
                pass

        return fig

    # Stockage de la trajectoire pour synchronisation
    @app.callback(
        Output(ids["trajectory_store"], "data"),
        [Input(ids["tau_slider"], "value"), Input(ids["delta_slider"], "value")],
    )
    def store_trajectory(tau, delta):
        """Stocke les données de trajectoire pour la synchronisation."""
        a, b, c, d = tau_delta_to_matrix(tau, delta)
        initial_condition = (1.0, 0.5)

        # Définir le système
        def system(state, t):
            x1_var, x2_var = state
            return [a * x1_var + b * x2_var, c * x1_var + d * x2_var]

        # Détecter le type de système pour adapter le temps d'intégration
        trace = a + d
        det = a * d - b * c

        is_centre = trace == 0 and det > 0
        is_mouvement_uniforme = trace == 0 and det == 0
        is_selle = det < 0
        is_unstable = trace > 0 or (det < 0 and trace > 0)

        # Adapter le temps d'intégration (mêmes valeurs que create_system_graph)
        if is_mouvement_uniforme:
            t = np.linspace(0, 8, 400)
        elif is_selle:
            t = np.linspace(0, 4, 300)
        elif is_centre:
            t = np.linspace(0, 4 * np.pi, 400)
        elif is_unstable:
            t = np.linspace(0, 3, 200)
        else:
            t = np.linspace(0, 16, 400)

        try:
            trajectory = odeint(system, list(initial_condition), t, full_output=False)
            return {
                "t": t.tolist(),
                "x1": trajectory[:, 0].tolist(),
                "x2": trajectory[:, 1].tolist(),
            }
        except:
            return {"t": [], "x1": [], "x2": []}
