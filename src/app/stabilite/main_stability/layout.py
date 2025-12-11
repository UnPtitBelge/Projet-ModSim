"""
Layout pour la page principale de stabilité.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html

from src.app.style.components.layout import (
    app_container,
    content_wrapper,
    graph_container,
    nav_button,
    section_card,
    side_by_side_container,
    side_by_side_last,
    spacing_section,
)
from src.app.style.components.tooltip import TOOLTIP_STYLE
from src.app.style.palette import PALETTE
from src.app.style.text import TEXT
from src.app.style.typography import TYPOGRAPHY

from .constants import get_ids


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
                    html.H1("Point d'équilibre et stabilité", style=TEXT["h1"]),
                    html.P(
                        "Explorez le comportement des systèmes dynamiques linéaires d'ordre 2 "
                        "en ajustant les paramètres τ (trace) et Δ (déterminant). "
                        "Les graphiques se mettent à jour en temps réel pour montrer "
                        "l'évolution temporelle et le portrait de phase associé. Un système est automatiquement généré en fonction des valeurs de τ et Δ.",
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
                                style={**TEXT["label"], "marginBottom": "8px"},
                            ),
                            dcc.Slider(
                                id=ids["tau_slider"],
                                min=-5,
                                max=5,
                                step=0.1,
                                value=0.0,
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
                                style={**TEXT["label"], "marginBottom": "8px"},
                            ),
                            dcc.Slider(
                                id=ids["delta_slider"],
                                min=-5,
                                max=5,
                                step=0.1,
                                value=0.0,
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
                                    dcc.Loading(
                                        id="main-stability-system-loading",
                                        type="default",
                                        children=[
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id=ids["system_graph"],
                                                        config={
                                                            "displayModeBar": False
                                                        },
                                                    )
                                                ],
                                                style=graph_container(),
                                            ),
                                        ],
                                    ),
                                ],
                                style=section_card(),
                            ),
                        ],
                        style=side_by_side_container(),
                    ),
                    # Diagramme de phase
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2(
                                        "Portrait de phase",
                                        style={**TEXT["h2"], "marginBottom": "12px"},
                                    ),
                                    dcc.Loading(
                                        id="main-stability-phase-loading",
                                        type="default",
                                        children=[
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id=ids["phase_diagram"],
                                                        config={
                                                            "displayModeBar": False
                                                        },
                                                    )
                                                ],
                                                style=graph_container(),
                                            ),
                                        ],
                                    ),
                                    # Légende interactive
                                    html.Div(
                                        [
                                            html.H3(
                                                "Légende du portrait de phase",
                                                style={
                                                    **TEXT["h3"],
                                                    "marginTop": "16px",
                                                    "marginBottom": "12px",
                                                },
                                            ),
                                            # Tooltips dbc (couleurs alignées sur la palette de l'app)
                                            dbc.Tooltip(
                                                "Point où les dérivées s'annulent (dx₁/dt = 0 et dx₂/dt = 0). Le système reste stationnaire en ce point (cas particulier du mouvement uniforme).",
                                                target=ids["legend_equilibrium"],
                                                placement="top",
                                                style=TOOLTIP_STYLE,
                                            ),
                                            dbc.Tooltip(
                                                "Solutions du système différentiel partant de différentes conditions initiales. Elles montrent comment l'état du système évolue dans le temps.",
                                                target=ids["legend_trajectories"],
                                                placement="top",
                                                style=TOOLTIP_STYLE,
                                            ),
                                            dbc.Tooltip(
                                                "Directions des vecteurs propres de la matrice. Les trajectoires s'alignent asymptotiquement avec ces directions pour les systèmes avec valeurs propres réelles.",
                                                target=ids["legend_eigenvectors"],
                                                placement="top",
                                                style=TOOLTIP_STYLE,
                                            ),
                                            dbc.Tooltip(
                                                "Courbes où une dérivée s'annule : orange (dx₁/dt = 0) et vert (dx₂/dt = 0). Elles divisent le plan en régions avec différents signes de dérivées.",
                                                target=ids["legend_isoclines"],
                                                placement="top",
                                                style=TOOLTIP_STYLE,
                                            ),
                                            dbc.Tooltip(
                                                "Vecteurs vitesse (dx/dt) en différents points du plan. Ils indiquent la direction et le sens du mouvement à chaque position.",
                                                target=ids["legend_vectors"],
                                                placement="top",
                                                style=TOOLTIP_STYLE,
                                            ),
                                            html.Div(
                                                [
                                                    # Point d'équilibre
                                                    html.Div(
                                                        [
                                                            html.Span(
                                                                "◆",
                                                                style={
                                                                    "color": PALETTE.accent_red,
                                                                    "fontSize": "20px",
                                                                    "marginRight": "8px",
                                                                },
                                                            ),
                                                            html.Span(
                                                                "Point d'équilibre",
                                                                id=ids[
                                                                    "legend_equilibrium"
                                                                ],
                                                                style={
                                                                    "textDecoration": "underline",
                                                                    "cursor": "pointer",
                                                                },
                                                            ),
                                                        ],
                                                        style={"marginBottom": "8px"},
                                                    ),
                                                    # Trajectoires
                                                    html.Div(
                                                        [
                                                            html.Span(
                                                                "━",
                                                                style={
                                                                    "color": PALETTE.primary,
                                                                    "fontSize": "20px",
                                                                    "marginRight": "8px",
                                                                },
                                                            ),
                                                            html.Span(
                                                                "Trajectoires",
                                                                id=ids[
                                                                    "legend_trajectories"
                                                                ],
                                                                style={
                                                                    "textDecoration": "underline",
                                                                    "cursor": "pointer",
                                                                },
                                                            ),
                                                        ],
                                                        style={"marginBottom": "8px"},
                                                    ),
                                                    # Directions propres
                                                    html.Div(
                                                        [
                                                            html.Span(
                                                                "- - -",
                                                                style={
                                                                    "color": PALETTE.stability_stable,
                                                                    "fontSize": "16px",
                                                                    "marginRight": "8px",
                                                                },
                                                            ),
                                                            html.Span(
                                                                "Droites vecteurs propres",
                                                                id=ids[
                                                                    "legend_eigenvectors"
                                                                ],
                                                                style={
                                                                    "textDecoration": "underline",
                                                                    "cursor": "pointer",
                                                                },
                                                            ),
                                                        ],
                                                        style={"marginBottom": "8px"},
                                                    ),
                                                    # Isoclines
                                                    html.Div(
                                                        [
                                                            html.Span(
                                                                "· · ·",
                                                                style={
                                                                    "color": PALETTE.third_light,
                                                                    "fontSize": "16px",
                                                                    "marginRight": "4px",
                                                                },
                                                            ),
                                                            html.Span(
                                                                " / ",
                                                                style={
                                                                    "marginRight": "4px",
                                                                },
                                                            ),
                                                            html.Span(
                                                                "· · ·",
                                                                style={
                                                                    "color": PALETTE.third_dark,
                                                                    "fontSize": "16px",
                                                                    "marginRight": "8px",
                                                                },
                                                            ),
                                                            html.Span(
                                                                "Isoclines",
                                                                id=ids[
                                                                    "legend_isoclines"
                                                                ],
                                                                style={
                                                                    "textDecoration": "underline",
                                                                    "cursor": "pointer",
                                                                },
                                                            ),
                                                        ],
                                                        style={"marginBottom": "8px"},
                                                    ),
                                                    # Champ de vecteurs
                                                    html.Div(
                                                        [
                                                            html.Span(
                                                                "→",
                                                                style={
                                                                    "color": PALETTE.secondary,
                                                                    "fontSize": "20px",
                                                                    "marginRight": "8px",
                                                                },
                                                            ),
                                                            html.Span(
                                                                "Champ de vecteurs",
                                                                id=ids[
                                                                    "legend_vectors"
                                                                ],
                                                                style={
                                                                    "textDecoration": "underline",
                                                                    "cursor": "pointer",
                                                                },
                                                            ),
                                                        ],
                                                        style={"marginBottom": "8px"},
                                                    ),
                                                ],
                                                style={
                                                    "display": "flex",
                                                    "flexDirection": "column",
                                                    "fontSize": "14px",
                                                },
                                            ),
                                        ],
                                        style={
                                            "marginTop": "16px",
                                            "padding": "16px",
                                            "backgroundColor": "#F9FAFB",
                                            "borderRadius": "8px",
                                            "border": "1px solid #E5E7EB",
                                        },
                                    ),
                                ],
                                style=section_card(),
                            ),
                        ],
                        style=side_by_side_last(),
                    ),
                ],
                style=spacing_section("top"),
            ),
            # Sections pédagogiques côte à côte
            html.Div(
                [
                    # Section pédagogique : Définitions des types de stabilité
                    html.Div(
                        [
                            html.H2(
                                "Définitions des types de stabilité", style=TEXT["h2"]
                            ),
                            html.Div(
                                [
                                    html.H3(
                                        "Stabilité asymptotique",
                                        style={
                                            **TEXT["h3"],
                                            "color": PALETTE.stability_stable,
                                        },
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
                                        style={
                                            **TEXT["h3"],
                                            "color": PALETTE.stability_marginal,
                                        },
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
                                        "Instabilité",
                                        style={
                                            **TEXT["h3"],
                                            "color": PALETTE.stability_unstable,
                                        },
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
                        style={
                            **section_card(),
                        },
                    ),
                    html.Div(
                        [
                            html.H2(
                                "Comment déterminer le type d'équilibre",
                                style=TEXT["h2"],
                            ),
                            html.P(
                                "Pour un système linéaire de dimension 2 représenté par la matrice A"
                            ),
                            html.Div(
                                "$$A = \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}$$",
                                className="tex2jax_process",
                            ),
                            html.H3(
                                "Nous devons calculer la trace (τ) et le déterminant (Δ):",
                                style=TEXT["h3"],
                            ),
                            html.P(
                                "La trace est égale à la somme des éléments diagonaux, et le déterminant est calculé comme suit:"
                            ),
                            html.Ul(
                                [
                                    html.Li(
                                        "$$\\tau = \\text{tr}(A) = a + d$$",
                                        className="tex2jax_process",
                                    ),
                                    html.Li(
                                        "$$\\Delta = \\det(A) = ad - bc$$",
                                        className="tex2jax_process",
                                    ),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                            html.H3("Il faut ensuite calculer les valeurs propres :", style=TEXT["h3"]),
                            html.Ul(
                                [
                                    html.Li(
                                        "Résoudre le polynôme caractéristique : $$\\lambda^2 - \\tau\\lambda + \\Delta = 0$$",
                                        className="tex2jax_process",
                                    ),
                                    html.Li(
                                        "Résoudre pour trouver les valeurs propres : $$\\lambda_{1,2} = \\frac{\\tau \\pm \\sqrt{\\tau^2 - 4\\Delta}}{2}$$",
                                        className="tex2jax_process",
                                    ),
                                ]
                            ),
                            html.H3("Avec ces données, nous pouvons déterminer le type d'équilibre:", style=TEXT["h3"]),
                            html.Ul(
                                [
                                    html.Li("Deux valeurs propres réelles négatives: Noeud stable"),
                                    html.Li("Deux valeurs propres réelles positives: Noeud instable"),
                                    html.Li("Deux valeurs propres complexes avec partie réelle négative: Foyer stable"),
                                    html.Li("Deux valeurs propres complexes avec partie réelle positive: Foyer instable"),   
                                    html.Li("Deux valeurs propres réelles de signes opposés: Selle"),       
                                    html.Li("Deux valeurs propres purement imaginaires: Centre"),
                                    html.Li("Présence d’une valeur propre nulle: ")
                                ]
                            ),
                        ],
                        style={
                            **section_card(),
                        },
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
                        style={
                            **section_card(),
                        },
                    ),
                ],
                style={"marginTop": "24px"},
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
                ],
                style={**section_card(), **spacing_section("bottom")},
            ),
            # Section: Navigation
            html.Div(
                [
                    html.Div(
                        [
                            html.A(
                                "→ Accéder au diagramme de Poincaré",
                                href="/poincare",
                                style=nav_button("primary"),
                            ),
                        ],
                        style=spacing_section("top"),
                    ),
                ],
                style=section_card(),
            ),
        ],
        style={
            **app_container(),
            **content_wrapper(),
        },
    )
