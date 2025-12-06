import dash
from dash import html

from src.app.style.components.layout import app_container, page_text_container
from src.app.style.text import TEXT

dash.register_page(
    __name__,
    path="/about",
    name="À propos",
    title="À propos",
    order=1,
    description="Informations générales, documentation et liens sur le projet.",
)

layout = html.Div(
    [
        html.H2("À propos", style=TEXT["h2"]),
        html.P(
            "Ce projet illustre l’analyse de la stabilité locale pour des systèmes "
            "linéaires continus du second ordre via le diagramme de Poincaré.",
            style=TEXT["p"],
        ),
        html.P(
            "L’application est conçue pour être extensible : d’autres pages pourront "
            "être ajoutées (ex. portraits de phase, diagrammes de bifurcation).",
            style=TEXT["p"],
        ),
        html.H3("Structure", style=TEXT["h3"]),
        html.Ul(
            [
                html.Li("src/app/app.py : point d’entrée multipage"),
                html.Li(
                    "src/app/poincare/ : modules spécifiques au diagramme de Poincaré"
                ),
                html.Li("src/app/pages/ : pages multipage natives (ce fichier, etc.)"),
            ],
            style=TEXT["p"],
        ),
        html.H3("Navigation", style=TEXT["h3"]),
        html.P(
            "Utilise les liens en haut de page pour revenir au diagramme principal ou explorer d’autres vues.",
            style=TEXT["p"],
        ),
        html.A(
            "Retour au diagramme de Poincaré",
            href="/poincare",
            style={"display": "inline-block", "marginTop": "18px"},
        ),
    ],
    style={
        **app_container(),
        **page_text_container(820),
        "padding": "24px",
    },
)
