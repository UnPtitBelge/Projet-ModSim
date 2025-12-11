"""
Stability page callbacks for displaying equilibrium properties and dynamics.

This module registers Dash callbacks that handle displaying computed properties for
each equilibrium type (eigenvalues, phase diagrams, system equations, etc.).

Callbacks are registered per-page using the page_key to create unique element IDs.
Each stability page displays:
- Eigenvalue information (type, values, nature)
- System ODE equation
- Phase portrait diagram
"""

from __future__ import annotations

from typing import Callable, Optional

import plotly.graph_objects as go
from dash import Dash, Input, Output, State, html, no_update

from src.app.style.palette import PALETTE
from src.app.style.text import TEXT

from .base_figures import create_phase_diagram, create_system_graph
from .base_layout import stability_ids
from .eigenvalue_utils import (calculate_eigenvalues, classify_equilibrium,
                               format_eigenvalue_display,
                               tau_delta_to_matrix_typed)


def register_stability_callbacks(
    app: Dash,
    page_key: str,
    tau: float,
    delta: float,
    create_phase_fig: Optional[Callable[[], go.Figure]] = None,
) -> None:
    """
    Register callbacks for a stability page (static display).

    Args:
        app: Dash application
        page_key: Page key for stability page
        tau: Trace value for this equilibrium type
        delta: Determinant value for this equilibrium type
        create_phase_fig: Optional function that returns the phase diagram figure.
                         If None, uses generic conversion from (tau, delta).
    """
    ids = stability_ids(page_key)

    # Affichage statique des valeurs propres
    @app.callback(
        Output(ids["eigenvalue_display"], "children"),
        Input(ids["eigenvalue_display"], "id"),
        prevent_initial_call=False,
    )
    def _display_eigenvalues(_eigenvalue_id: Optional[str]):
        """Affiche les valeurs propres pour ce type d'équilibre."""
        eigenvalue_info = format_eigenvalue_display(tau, delta)

        return [
            html.Div(
                [
                    html.Strong(
                        "Type de point d'équilibre : ", style={"color": PALETTE.primary}
                    ),
                    html.Span(eigenvalue_info["type"]),
                ],
                style={"marginBottom": "1rem"},
            ),
            html.Div(
                [
                    html.Strong("Valeurs propres : "),
                    html.Span(eigenvalue_info["eigenvalues"]),
                ],
                style={"marginBottom": "0.5rem"},
            ),
            html.Div(
                [
                    html.Strong("Nature : "),
                    html.Span(eigenvalue_info["nature"]),
                ]
            ),
        ]

    # Affichage de l'équation différentielle
    @app.callback(
        Output(ids["ode_display"], "children"),
        Input(ids["ode_display"], "id"),
        prevent_initial_call=False,
    )
    def _display_ode(_ode_id: Optional[str]):
        """Affiche l'équation différentielle du système."""
        a, b, c, d = tau_delta_to_matrix_typed(tau, delta, page_key)

        # Formater les coefficients pour l'affichage
        def format_coeff(val: float) -> str:
            if val == 0:
                return "0"
            elif val == 1:
                return ""
            elif val == -1:
                return "-"
            else:
                return f"{val:.2f}" if val != int(val) else str(int(val))

        def term(coeff: float, var: str) -> str:
            if coeff == 0:
                return ""
            coeff_str = format_coeff(coeff)
            if coeff > 0:
                return f"+ {coeff_str}{var}" if coeff_str else f"+ {var}"
            else:
                return f"- {coeff_str[1:]}{var}" if len(coeff_str) > 1 else f"- {var}"

        # Construire les équations
        x1_terms = []
        if b != 0:
            if b > 0:
                x1_terms.append(f"+ {format_coeff(b)}x₂" if format_coeff(b) else "+ x₂")
            else:
                x1_terms.append(
                    f"- {format_coeff(-b)}x₂" if format_coeff(-b) else "- x₂"
                )
        if a > 0:
            x1_terms.insert(0, f"{format_coeff(a)}x₁" if format_coeff(a) else "x₁")
        elif a < 0:
            x1_terms.insert(
                0, f"- {format_coeff(-a)}x₁" if format_coeff(-a) else "- x₁"
            )
        else:
            pass

        x2_terms = []
        if c != 0:
            if c > 0:
                x2_terms.append(f"+ {format_coeff(c)}x₁" if format_coeff(c) else "+ x₁")
            else:
                x2_terms.append(
                    f"- {format_coeff(-c)}x₁" if format_coeff(-c) else "- x₁"
                )
        if d > 0:
            x2_terms.insert(0, f"{format_coeff(d)}x₂" if format_coeff(d) else "x₂")
        elif d < 0:
            x2_terms.insert(
                0, f"- {format_coeff(-d)}x₂" if format_coeff(-d) else "- x₂"
            )
        else:
            pass

        x1_eq = " ".join(x1_terms) if x1_terms else "0"
        x2_eq = " ".join(x2_terms) if x2_terms else "0"

        # Nettoyer les espaces excessifs
        x1_eq = x1_eq.strip().lstrip("+ ").replace("  ", " ")
        x2_eq = x2_eq.strip().lstrip("+ ").replace("  ", " ")

        # Utiliser MathJax pour afficher l'EDO
        mathjax_content = f"""
        $$\\dot{{x}}_1 = {x1_eq}$$
        $$\\dot{{x}}_2 = {x2_eq}$$
        """

        return html.Div(
            children=mathjax_content,
        )

    # Diagramme de phase (statique)
    @app.callback(
        Output(ids["phase"], "figure"),
        Input(ids["phase"], "id"),
        prevent_initial_call=False,
    )
    def _display_phase_diagram(_phase_id: Optional[str]) -> go.Figure:
        """Affiche le diagramme de phase pour ce type d'équilibre."""
        # Si une fonction personnalisée est fournie, l'utiliser
        if create_phase_fig is not None:
            return create_phase_fig()

        # Sinon, utiliser la conversion typée basée sur page_key
        a, b, c, d = tau_delta_to_matrix_typed(tau, delta, page_key)
        eq_type = classify_equilibrium(tau, delta)
        title = f"Diagramme de phase: {eq_type}"

        # Créer le diagramme avec les paramètres calculés
        return create_phase_diagram(a, b, c, d, title=title)

    # Graphe temporel du système (statique)
    @app.callback(
        Output(ids["system_graph"], "figure"),
        Input(ids["system_graph"], "id"),
        prevent_initial_call=False,
    )
    def _display_system_graph(_system_graph_id: Optional[str]) -> go.Figure:
        """Affiche le graphe temporel x₁(t) et x₂(t) pour ce type d'équilibre."""
        # Obtenir les coefficients de la matrice
        a, b, c, d = tau_delta_to_matrix_typed(tau, delta, page_key)
        eq_type = classify_equilibrium(tau, delta)
        title = f"Évolution temporelle: {eq_type}"

        # Créer le graphe avec les paramètres calculés
        return create_system_graph(a, b, c, d, title=title)
