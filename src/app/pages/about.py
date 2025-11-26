"""
Page multipage native Dash : À propos.

Cette page fournit un espace pour de la documentation, des explications ou des liens
dans l'application multipage. Elle est enregistrée automatiquement grâce à
dash.register_page quand Dash est lancé avec use_pages=True.

Si tu avais un enregistrement manuel de la page dans app.py via dash.register_page(...),
tu peux le retirer pour éviter les doublons. Le système détecte tous les fichiers
du dossier `pages/` qui appellent `dash.register_page(__name__, ...)`.

Attributs enregistrés :
- path        : /about
- name        : À propos (affiché dans une navigation générée dynamiquement)
- title       : Titre de la page (onglet navigateur)
- order       : Ordre d’apparition dans la barre de navigation (croissant)
- description : Courte description (utilisable par certains outils ou SEO)

Layout :
La variable globale `layout` doit exister pour que Dash puisse l’inclure dans
`dash.page_container`.
"""

import dash
from dash import html

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
        html.H2("À propos"),
        html.P(
            "Ce projet illustre l’analyse de la stabilité locale pour des systèmes "
            "linéaires continus du second ordre via le diagramme de Poincaré."
        ),
        html.P(
            "L’application est conçue pour être extensible : d’autres pages pourront "
            "être ajoutées (ex. portraits de phase, diagrammes de bifurcation)."
        ),
        html.H3("Structure"),
        html.Ul(
            [
                html.Li("src/app/app.py : point d’entrée multipage"),
                html.Li(
                    "src/app/poincare/ : modules spécifiques au diagramme de Poincaré"
                ),
                html.Li("src/app/pages/ : pages multipage natives (ce fichier, etc.)"),
            ]
        ),
        html.H3("Navigation"),
        html.P(
            "Utilise les liens en haut de page pour revenir au diagramme principal ou explorer d’autres vues."
        ),
        html.A(
            "Retour au diagramme de Poincaré",
            href="/",
            style={"display": "inline-block", "marginTop": "18px"},
        ),
    ],
    style={
        "maxWidth": "820px",
        "padding": "24px",
        "fontFamily": "Arial, sans-serif",
        "lineHeight": "1.45",
        "fontSize": "0.95rem",
    },
)
