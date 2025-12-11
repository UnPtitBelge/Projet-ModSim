"""
Layout de la page du problème à trois corps.

Crée l'interface utilisateur pour la visualisation et l'interaction avec
la simulation du problème à trois corps.
"""

from __future__ import annotations

from dash import dcc, html

from src.app.chaos.plots import build_three_body_figure_with_data
from src.app.style.components.layout import (action_button, alert_box,
                                             app_container, content_wrapper,
                                             graph_container,
                                             loading_container, section_card, spacing_section,)
from src.app.style.text import TEXT


def build_layout() -> html.Div:
    """
    Construit le layout complet de la page du problème à trois corps.

    Inclut:
    - Introduction théorique au problème
    - Contexte historique
    - Simulation interactive avec animation
    - Explication des équations mathématiques
    - Discussion sur l'instabilité chaotique

    Returns:
        Composant Div contenant le layout complet de la page
    """
    return html.Div(
        [
            # Contexte historique en premier
            html.Div(
                [
                    html.H2("Contexte historique et découverte", style=TEXT["h2"]),
                    html.P(
                        [
                            "En 1885, le roi Oscar II de Suède lança un concours pour encourager la résolution ",
                            "du problème de la stabilité du système solaire. Poincaré, en tentant de répondre, ",
                            "découvrit que même un système à trois corps peut générer un comportement ",
                            html.Strong("imprévisible"),
                            ", car les trajectoires deviennent hypersensibles aux conditions initiales. ",
                            "Cette découverte marqua la naissance de la théorie du chaos et bouleversa ",
                            "la vision déterministe de la mécanique classique.",
                        ],
                        style=TEXT["p"],
                        className="tex2jax_process",
                    ),
                ],
                style={**section_card(), **spacing_section("bottom")},
            ),
            # Section englobante du problème à trois corps
            html.Div(
                [
                    html.H2("Le problème à trois corps", style=TEXT["h2"]),
                    html.P(
                        [
                            "Le problème à trois corps consiste à prédire le mouvement de trois corps célestes ",
                            "soumis uniquement à la gravité. Ce problème fut découvert ",
                            html.Strong("chaotique"),
                            " par Henri Poincaré à la fin du 19",
                            html.Sup("e"),
                            " siècle : malgré la simplicité apparente du système, une variation ",
                            "infime des conditions initiales conduit à des trajectoires radicalement différentes, ",
                            "rendant toute prédiction à long terme impossible.",
                        ],
                        style=TEXT["p"],
                        className="tex2jax_process",
                    ),
                    # Simulation interactive
                    html.Div(
                        [
                            html.H3("Simulation interactive", style=TEXT["h3"]),
                            html.P(
                                [
                                    "Utilisez les boutons ci-dessous pour explorer différentes configurations. ",
                                    "Le bouton ",
                                    html.Strong("Générer"),
                                    " ajoute de petites perturbations aléatoires (±5%) aux positions initiales, ",
                                    "tandis que ",
                                    html.Strong("Reset"),
                                    " revient à la configuration de base.",
                                ],
                                style=TEXT["p"],
                                className="tex2jax_process",
                            ),
                            html.P(
                                [
                                    "⚠️ Attention : appuyer sur ces boutons pendant l'animation ne fonctionne pas. ",
                                    "Vous devez d'abord laisser l'animation se terminer ou la mettre en pause ",
                                    "(ou appuyer sur ",
                                    html.Em("reset"),
                                    " dans les contrôles de l'animation).",
                                ],
                                style=alert_box("warning"),
                                className="tex2jax_process",
                            ),
                            html.Div(
                                [
                                    html.Button(
                                        "Générer",
                                        id="chaos-restart-button",
                                        n_clicks=0,
                                        style=action_button(),
                                    ),
                                    html.Button(
                                        "↻ Reset",
                                        id="chaos-reset-button",
                                        n_clicks=0,
                                        style={**action_button(), **spacing_section("left")},
                                        title="Réinitialiser aux positions de base",
                                    ),
                                ],
                            ),
                            html.Div(
                                id="chaos-initial-conditions",
                                style=section_card(),
                            ),
                            dcc.Loading(
                                id="chaos-loading",
                                type="default",
                                children=[
                                    html.Div(
                                        dcc.Graph(
                                            id="chaos-three-body-graph",
                                            figure=build_three_body_figure_with_data()[
                                                0
                                            ],
                                            config={"displayModeBar": False},
                                        ),
                                        style=graph_container(),
                                    ),
                                ],
                                style=loading_container(),
                            ),
                        ],
                        style=section_card(),
                    ),
                    # Équations du mouvement
                    html.Div(
                        [
                            html.H3("Les équations du mouvement", style=TEXT["h3"]),
                            html.P(
                                [
                                    "Chaque corps $i$ de masse $m_i$ obéit à la loi de la gravitation universelle. ",
                                    "L'accélération subie par le corps $i$ est donnée par :",
                                ],
                                style=TEXT["p"],
                                className="tex2jax_process",
                            ),
                            html.Div(
                                r"$$\mathbf{a}_i = G \sum_{j \ne i} \frac{m_j \, (\mathbf{r}_j - \mathbf{r}_i)}{|\mathbf{r}_j - \mathbf{r}_i|^3}$$",
                                style=TEXT["p"],
                                className="tex2jax_process",
                            ),
                            html.P(
                                [
                                    "où $G$ est la constante de gravitation, et $\\mathbf{r}_i$, $\\mathbf{r}_j$ ",
                                    "sont les positions respectives des corps. ",
                                    "Ce système d'équations différentielles n'admet pas de solution analytique générale ",
                                    "et doit être intégré numériquement.",
                                ],
                                style=TEXT["p"],
                                className="tex2jax_process",
                            ),
                        ],
                        style={**section_card(), **spacing_section()},
                    ),
                    # Sensibilité aux conditions initiales
                    html.Div(
                        [
                            html.H3(
                                "Sensibilité aux conditions initiales", style=TEXT["h3"]
                            ),
                            html.P(
                                [
                                    "Le caractère chaotique se manifeste par une ",
                                    html.Strong("divergence exponentielle"),
                                    " des trajectoires : deux systèmes identiques à 0.01% près évolueront de façon ",
                                    "complètement différente après un temps relativement court. C'est cette sensibilité ",
                                    "qui rend impossible toute prédiction précise sur le long terme, même avec ",
                                    "des ordinateurs très puissants.",
                                ],
                                style=TEXT["p"],
                                className="tex2jax_process",
                            ),
                        ],
                        style=section_card(),
                    ),
                ],
                style=section_card(),
            ),
            # Conclusion globale sur le chaos
            html.Div(
                [
                    html.H2(
                        "Comprendre le chaos : l'ordre dans le désordre",
                        style=TEXT["h2"],
                    ),
                    html.P(
                        [
                            "Bien que les systèmes chaotiques soient ",
                            html.Strong("déterministes"),
                            " (les mêmes conditions initiales produisent toujours le même résultat), ",
                            "leur ",
                            html.Strong("extrême sensibilité"),
                            " aux conditions initiales les rend imprévisibles en pratique. ",
                            "Une erreur de mesure infinitésimale se propage exponentiellement, ",
                            "rendant toute prédiction à long terme impossible.",
                        ],
                        style=TEXT["p"],
                        className="tex2jax_process",
                    ),
                    html.P(
                        [
                            "Cependant, le chaos n'est pas synonyme d'anarchie totale. Les scientifiques ont découvert que ",
                            "les systèmes chaotiques présentent des ",
                            html.Strong("structures récurrentes"),
                            " appelées ",
                            html.Em("attracteurs étranges"),
                            ". Ces structures révèlent que, malgré l'imprévisibilité des trajectoires individuelles, ",
                            "le système évolue dans un espace de phase délimité avec des patterns statistiques stables.",
                        ],
                        style=TEXT["p"],
                        className="tex2jax_process",
                    ),
                    html.P(
                        [
                            "Cette découverte a révolutionné de nombreux domaines : météorologie (l'effet papillon), ",
                            "économie, biologie des populations, neurosciences, et même l'étude des systèmes planétaires. ",
                            "Au lieu de chercher à prédire l'évolution exacte d'un système chaotique, ",
                            "les scientifiques analysent désormais ses ",
                            html.Strong("propriétés statistiques"),
                            ", ses attracteurs, et les transitions entre différents régimes dynamiques.",
                        ],
                        style=TEXT["p"],
                        className="tex2jax_process",
                    ),
                ],
                style={**section_card(), **spacing_section()},
            ),
        ],
        style={
            **app_container(),
            **content_wrapper(),
        },
    )
