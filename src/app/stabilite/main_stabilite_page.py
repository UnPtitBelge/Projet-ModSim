"""
Module principal pour la page d'analyse interactive de stabilité.

Fournit une interface interactive permettant d'explorer le comportement
des systèmes dynamiques linéaires 2D en fonction de leurs paramètres (τ, Δ).
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dcc, html
from scipy.integrate import odeint

from src.app.style.components.layout import (content_wrapper, graph_container,
                                             section_card)
from src.app.style.palette import PALETTE
from src.app.style.text import TEXT
from src.app.style.typography import TYPOGRAPHY

from .base_figures import create_phase_diagram, create_system_graph
from .eigenvalue_utils import (calculate_eigenvalues, classify_equilibrium,
                               format_eigenvalue_display, tau_delta_to_matrix)

# ============================================================================
# IDENTIFIANTS
# ============================================================================


def get_ids():
    """Retourne les identifiants des composants de la page."""
    return {
        "tau_slider": "main-stab-tau-slider",
        "delta_slider": "main-stab-delta-slider",
        "system_graph": "main-stab-system-graph",
        "phase_diagram": "main-stab-phase-diagram",
        "eigenvalue_display": "main-stab-eigenvalue-display",
        "ode_display": "main-stab-ode-display",
        "equilibrium_type": "main-stab-equilibrium-type",
    }


# ============================================================================
# LAYOUT
# ============================================================================


def build_layout() -> html.Div:
    """
    Construit le layout complet de la page d'analyse interactive.

    Returns:
        Layout Dash complet avec sliders, graphiques et contenu pédagogique
    """
    ids = get_ids()

    return html.Div(
        [
            # Titre et introduction
            html.Div(
                [
                    html.H1(
                        "Analyse de stabilité des systèmes linéaires", style=TEXT["h1"]
                    ),
                    html.P(
                        "Explorez le comportement des systèmes dynamiques linéaires d'ordre 2 "
                        "en ajustant les paramètres τ (trace) et Δ (déterminant). "
                        "Les graphiques se mettent à jour en temps réel pour montrer "
                        "l'évolution temporelle et le portrait de phase.",
                        style=TEXT["p"],
                    ),
                ],
                style=section_card(),
            ),
            # Section de contrôle des paramètres
            html.Div(
                [
                    html.H2("Paramètres du système", style=TEXT["h2"]),
                    # Contrôles pour τ (trace)
                    html.Div(
                        [
                            html.Label(
                                "τ (Trace) :",
                                style={
                                    **TEXT["p"],
                                    "fontWeight": str(TYPOGRAPHY.weight_semibold),
                                    "marginBottom": "8px",
                                },
                            ),
                            dcc.Slider(
                                id=ids["tau_slider"],
                                min=-5,
                                max=5,
                                step=0.1,
                                value=1.0,
                                marks={i: str(i) for i in range(-5, 6)},
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": True,
                                },
                            ),
                        ],
                        style={"marginBottom": "24px"},
                    ),
                    # Contrôles pour Δ (déterminant)
                    html.Div(
                        [
                            html.Label(
                                "Δ (Déterminant) :",
                                style={
                                    **TEXT["p"],
                                    "fontWeight": str(TYPOGRAPHY.weight_semibold),
                                    "marginBottom": "8px",
                                },
                            ),
                            dcc.Slider(
                                id=ids["delta_slider"],
                                min=-5,
                                max=10,
                                step=0.1,
                                value=2.0,
                                marks={i: str(i) for i in range(-5, 11)},
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": True,
                                },
                            ),
                        ],
                        style={"marginBottom": "16px"},
                    ),
                    # Affichage du type d'équilibre
                    html.Div(
                        [
                            html.H3(
                                "Type d'équilibre : ",
                                style={
                                    **TEXT["h3"],
                                    "display": "inline",
                                    "marginRight": "12px",
                                },
                            ),
                            html.Span(
                                id=ids["equilibrium_type"],
                                style={
                                    "fontSize": f"{TYPOGRAPHY.size_xl}rem",
                                    "fontWeight": str(TYPOGRAPHY.weight_bold),
                                    "color": PALETTE.primary,
                                },
                            ),
                        ],
                        style={"marginTop": "16px", "marginBottom": "16px"},
                    ),
                    # Affichage de l'EDO
                    html.Div(
                        [
                            html.H3("Équations différentielles :", style=TEXT["h3"]),
                            html.Div(id=ids["ode_display"], style={"marginTop": "8px"}),
                        ],
                        style={"marginTop": "16px"},
                    ),
                    # Affichage des valeurs propres
                    html.Div(
                        [
                            html.H3("Valeurs propres :", style=TEXT["h3"]),
                            html.Div(
                                id=ids["eigenvalue_display"], style={"marginTop": "8px"}
                            ),
                        ],
                        style={"marginTop": "16px"},
                    ),
                ],
                style=section_card(),
            ),
            # Section des graphiques
            html.Div(
                [
                    # Graphique temporel
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2("Évolution temporelle", style=TEXT["h2"]),
                                    html.Div(
                                        [
                                            dcc.Graph(
                                                id=ids["system_graph"],
                                                config={"displayModeBar": False},
                                            )
                                        ],
                                        style=graph_container(),
                                    ),
                                ],
                                style=section_card(),
                            ),
                        ],
                        style={
                            "width": "48%",
                            "display": "inline-block",
                            "marginRight": "4%",
                            "verticalAlign": "top",
                        },
                    ),
                    # Diagramme de phase
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2("Portrait de phase", style=TEXT["h2"]),
                                    html.Div(
                                        [
                                            dcc.Graph(
                                                id=ids["phase_diagram"],
                                                config={"displayModeBar": False},
                                            )
                                        ],
                                        style=graph_container(),
                                    ),
                                ],
                                style=section_card(),
                            ),
                        ],
                        style={
                            "width": "48%",
                            "display": "inline-block",
                            "verticalAlign": "top",
                        },
                    ),
                ],
                style={"marginTop": "24px"},
            ),
            # Section pédagogique : Définitions des types de stabilité
            html.Div(
                [
                    html.H2("Définitions des types de stabilité", style=TEXT["h2"]),
                    html.Div(
                        [
                            html.H3(
                                "Stabilité asymptotique",
                                style={**TEXT["h3"], "color": "#27ae60"},
                            ),
                            html.P(
                                [
                                    "Un point d'équilibre est ",
                                    html.Strong("asymptotiquement stable"),
                                    " si toutes les trajectoires démarrant près de ce point convergent vers lui lorsque ",
                                    html.Em("t → ∞"),
                                    ". Pour un système linéaire, cela se produit lorsque toutes les valeurs propres ont une ",
                                    html.Strong("partie réelle négative"),
                                    ".",
                                ],
                                style=TEXT["p"],
                            ),
                            html.Ul(
                                [
                                    html.Li(
                                        "Foyer stable : valeurs propres complexes avec Re(λ) < 0 (spirale convergente)",
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        "Nœud stable : valeurs propres réelles négatives (convergence directe)",
                                        style=TEXT["p"],
                                    ),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                        ],
                        style={"marginBottom": "20px"},
                    ),
                    html.Div(
                        [
                            html.H3(
                                "Stabilité (marginale)",
                                style={**TEXT["h3"], "color": "#f39c12"},
                            ),
                            html.P(
                                [
                                    "Un point d'équilibre est ",
                                    html.Strong("stable"),
                                    " (mais pas asymptotiquement) si les trajectoires restent bornées près du point sans nécessairement y converger. "
                                    "Cela se produit pour un ",
                                    html.Strong("centre"),
                                    " avec des valeurs propres purement imaginaires (oscillations non amorties).",
                                ],
                                style=TEXT["p"],
                            ),
                        ],
                        style={"marginBottom": "20px"},
                    ),
                    html.Div(
                        [
                            html.H3(
                                "Instabilité", style={**TEXT["h3"], "color": "#e74c3c"}
                            ),
                            html.P(
                                [
                                    "Un point d'équilibre est ",
                                    html.Strong("instable"),
                                    " si au moins une trajectoire s'éloigne du point. Cela se produit lorsqu'au moins une valeur propre a une ",
                                    html.Strong("partie réelle positive"),
                                    ".",
                                ],
                                style=TEXT["p"],
                            ),
                            html.Ul(
                                [
                                    html.Li(
                                        "Foyer instable : valeurs propres complexes avec Re(λ) > 0 (spirale divergente)",
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        "Nœud instable : valeurs propres réelles positives (divergence directe)",
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        "Selle : valeurs propres réelles de signes opposés (stabilité mixte)",
                                        style=TEXT["p"],
                                    ),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                        ],
                        style={"marginBottom": "20px"},
                    ),
                ],
                style=section_card(),
            ),
            # Section pédagogique : Impact des paramètres
            html.Div(
                [
                    html.H2("Impact des paramètres τ et Δ", style=TEXT["h2"]),
                    html.P(
                        [
                            "Pour un système linéaire ",
                            html.Span(
                                "$\\dot{\\mathbf{x}} = A\\mathbf{x}$",
                                className="tex2jax_process",
                            ),
                            ", le comportement est déterminé par les valeurs propres de la matrice A, "
                            "qui dépendent de sa trace τ = tr(A) et de son déterminant Δ = det(A).",
                        ],
                        style=TEXT["p"],
                    ),
                    html.Div(
                        [
                            html.H3("Trace (τ) :", style=TEXT["h3"]),
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            html.Strong("τ > 0"),
                                            " : système avec tendance à l'instabilité (au moins une valeur propre peut avoir partie réelle positive)",
                                        ],
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        [
                                            html.Strong("τ = 0"),
                                            " : cas marginal (centre, mouvement uniforme)",
                                        ],
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        [
                                            html.Strong("τ < 0"),
                                            " : système avec tendance à la stabilité (valeurs propres avec partie réelle négative)",
                                        ],
                                        style=TEXT["p"],
                                    ),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                        ],
                        style={"marginBottom": "20px"},
                    ),
                    html.Div(
                        [
                            html.H3("Déterminant (Δ) :", style=TEXT["h3"]),
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            html.Strong("Δ < 0"),
                                            " : valeurs propres réelles de signes opposés → ",
                                            html.Strong("selle"),
                                            " (instable)",
                                        ],
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        [
                                            html.Strong("Δ = 0"),
                                            " : au moins une valeur propre nulle (cas dégénéré)",
                                        ],
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        [
                                            html.Strong("0 < Δ < τ²/4"),
                                            " : valeurs propres réelles de même signe → ",
                                            html.Strong("nœud"),
                                            " (stable si τ > 0, instable si τ < 0)",
                                        ],
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        [
                                            html.Strong("Δ > τ²/4"),
                                            " : valeurs propres complexes conjuguées → ",
                                            html.Strong("foyer"),
                                            " (stable si τ > 0, instable si τ < 0)",
                                        ],
                                        style=TEXT["p"],
                                    ),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                        ]
                    ),
                ],
                style=section_card(),
            ),
            # Section : Exemples de la vie réelle
            html.Div(
                [
                    html.H2(
                        "Exemples de systèmes d'ordre 2 dans la vie réelle",
                        style=TEXT["h2"],
                    ),
                    html.Div(
                        [
                            html.H3(
                                "1. Système masse-ressort-amortisseur", style=TEXT["h3"]
                            ),
                            html.P(
                                [
                                    "Le système mécanique classique suit l'équation : ",
                                    html.Div(
                                        "$$m\\ddot{x} + c\\dot{x} + kx = 0$$",
                                        className="tex2jax_process",
                                    ),
                                ],
                                style=TEXT["p"],
                            ),
                            html.P(
                                [
                                    "En posant ",
                                    html.Span(
                                        "$x_1 = x$",
                                        className="tex2jax_process",
                                        style={"display": "inline"},
                                    ),
                                    " et ",
                                    html.Span(
                                        "$x_2 = \\dot{x}$",
                                        className="tex2jax_process",
                                        style={"display": "inline"},
                                    ),
                                    ", on obtient : ",
                                    html.Div(
                                        "$$\\tau = -\\frac{c}{m}, \\quad \\Delta = \\frac{k}{m}$$",
                                        className="tex2jax_process",
                                    ),
                                ],
                                style=TEXT["p"],
                            ),
                            html.Ul(
                                [
                                    html.Li(
                                        "c = 0 (pas d'amortissement) : centre (oscillations perpétuelles)",
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        "c > 0, c² < 4mk : foyer stable (oscillations amorties)",
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        "c > 0, c² > 4mk : nœud stable (retour sans oscillation)",
                                        style=TEXT["p"],
                                    ),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                        ],
                        style={"marginBottom": "24px"},
                    ),
                    html.Div(
                        [
                            html.H3("2. Circuit RLC série", style=TEXT["h3"]),
                            html.P(
                                [
                                    "L'équation du circuit est : ",
                                    html.Div(
                                        "$$L\\ddot{q} + R\\dot{q} + \\frac{1}{C}q = 0$$",
                                        className="tex2jax_process",
                                    ),
                                ],
                                style=TEXT["p"],
                            ),
                            html.P(
                                [
                                    "Avec ",
                                    html.Span(
                                        "$x_1 = q$",
                                        className="tex2jax_process",
                                        style={"display": "inline"},
                                    ),
                                    " (charge) et ",
                                    html.Span(
                                        "$x_2 = \\dot{q}$",
                                        className="tex2jax_process",
                                        style={"display": "inline"},
                                    ),
                                    " (courant) : ",
                                    html.Div(
                                        "$$\\tau = -\\frac{R}{L}, \\quad \\Delta = \\frac{1}{LC}$$",
                                        className="tex2jax_process",
                                    ),
                                ],
                                style=TEXT["p"],
                            ),
                            html.Ul(
                                [
                                    html.Li(
                                        "R = 0 : oscillations électriques non amorties (centre)",
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        "R > 0, R² < 4L/C : oscillations amorties (foyer stable)",
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        "R > 0, R² > 4L/C : décroissance exponentielle (nœud stable)",
                                        style=TEXT["p"],
                                    ),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                        ],
                        style={"marginBottom": "24px"},
                    ),
                    html.Div(
                        [
                            html.H3(
                                "3. Système proie-prédateur (linéarisé)",
                                style=TEXT["h3"],
                            ),
                            html.P(
                                [
                                    "Le modèle de Lotka-Volterra linéarisé autour d'un point d'équilibre donne un système dont la stabilité "
                                    "dépend des taux de reproduction et de prédation. Un équilibre peut être :"
                                ],
                                style=TEXT["p"],
                            ),
                            html.Ul(
                                [
                                    html.Li(
                                        "Centre : oscillations cycliques de populations",
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        "Foyer stable : retour oscillant à l'équilibre",
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        "Selle : équilibre instable (extinction d'une espèce)",
                                        style=TEXT["p"],
                                    ),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                        ],
                        style={"marginBottom": "24px"},
                    ),
                    html.Div(
                        [
                            html.H3("4. Pendule simple (linéarisé)", style=TEXT["h3"]),
                            html.P(
                                [
                                    "Près de l'équilibre vertical : ",
                                    html.Div(
                                        "$$\\ddot{\\theta} + \\frac{g}{L}\\theta = 0$$",
                                        className="tex2jax_process",
                                    ),
                                    " (centre, oscillations harmoniques)",
                                ],
                                style=TEXT["p"],
                            ),
                            html.P(
                                [
                                    "Avec frottement : ",
                                    html.Div(
                                        "$$\\ddot{\\theta} + \\gamma\\dot{\\theta} + \\frac{g}{L}\\theta = 0$$",
                                        className="tex2jax_process",
                                    ),
                                    " (foyer stable ou nœud stable selon γ)",
                                ],
                                style=TEXT["p"],
                            ),
                        ],
                        style={"marginBottom": "24px"},
                    ),
                    html.Div(
                        [
                            html.H3("5. Systèmes de contrôle", style=TEXT["h3"]),
                            html.P(
                                [
                                    "En automatique, la stabilité d'un système asservi est cruciale. "
                                    "Les paramètres τ et Δ dépendent des gains du contrôleur. "
                                    "Un mauvais réglage peut mener à :"
                                ],
                                style=TEXT["p"],
                            ),
                            html.Ul(
                                [
                                    html.Li(
                                        "Foyer stable : réponse oscillante mais contrôlée",
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        "Nœud stable : réponse optimale sans dépassement",
                                        style=TEXT["p"],
                                    ),
                                    html.Li(
                                        "Foyer instable : oscillations croissantes (système instable)",
                                        style=TEXT["p"],
                                    ),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                        ]
                    ),
                ],
                style=section_card(),
            ),
            # Section: Navigation
            html.Div(
                [
                    html.Div(
                        [
                            html.A(
                                "→ Accéder au diagramme de Poincaré",
                                href="/poincare",
                                style={
                                    "display": "inline-block",
                                    "padding": "12px 24px",
                                    "backgroundColor": PALETTE.primary,
                                    "color": PALETTE.surface,
                                    "textDecoration": "none",
                                    "borderRadius": "8px",
                                    "fontWeight": "600",
                                    "marginRight": "12px",
                                },
                            ),
                        ],
                        style={"marginTop": "24px"},
                    ),
                ],
                style=section_card(),
            ),
        ],
        style=content_wrapper(),
    )


# ============================================================================
# CALLBACKS
# ============================================================================


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

    # Génération du diagramme de phase
    @app.callback(
        Output(ids["phase_diagram"], "figure"),
        [Input(ids["tau_slider"], "value"), Input(ids["delta_slider"], "value")],
    )
    def update_phase_diagram(tau, delta):
        """Génère le diagramme de phase."""
        a, b, c, d = tau_delta_to_matrix(tau, delta)
        title = "Portrait de phase"

        return create_phase_diagram(a, b, c, d, title)
