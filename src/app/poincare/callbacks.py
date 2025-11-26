"""
Callbacks pour le diagramme de Poincaré : survol et clic (mise en évidence des zones).

API:
    ZoneColors              dataclass des couleurs (base, hover, click)
    DEFAULT_ZONE_LABELS     mapping curveNumber -> label (fr)
    register_callbacks(...) attache les callbacks à l'application Dash

Principe:
- On duplique la figure immuable (base_figure) à chaque interaction.
- Priorité des couleurs : clic > hover > base.
- Indices de traces: 0 parabole, 1..5 zones.

Les IDs attendus dans le layout:
    Graph        : "poincaré-graph"
    Survol texte : "output-temp-hover"
    Clic texte   : "output-temp-click"
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Dict, Optional

import plotly.graph_objs as go
from dash import Dash, Input, Output  # type: ignore


@dataclass(frozen=True)
class ZoneColors:
    base: str = "rgba(210, 70, 70, 0.35)"
    hover: str = "rgba(240, 150, 150, 0.55)"
    click: str = "rgba(150, 30, 30, 0.65)"


# Labels par défaut (français)
DEFAULT_ZONE_LABELS: Dict[int, str] = {
    0: "Parabole",
    1: "Zone supérieure gauche",
    2: "Zone supérieure droite",
    3: "Zone inférieure gauche",
    4: "Zone inférieure droite",
    5: "Zone inférieure",
}


def register_callbacks(
    app: Dash,
    base_figure: go.Figure,
    colors: Optional[ZoneColors] = None,
    zone_labels: Optional[Dict[int, str]] = None,
    graph_id: str = "poincaré-graph",
    hover_output_id: str = "output-temp-hover",
    click_output_id: str = "output-temp-click",
) -> None:
    """
    Attache les callbacks d'interaction (hover + click) sur la figure Poincaré.

    Paramètres:
        app            : instance Dash
        base_figure    : figure immuable (parabole + zones)
        colors         : configuration des couleurs (optionnel)
        zone_labels    : dictionnaire curveNumber -> label (optionnel)
        graph_id       : id du composant dcc.Graph
        hover_output_id: id du conteneur texte de survol
        click_output_id: id du conteneur texte de clic
    """
    color_cfg = colors or ZoneColors()
    labels = zone_labels or DEFAULT_ZONE_LABELS

    @app.callback(
        Output(graph_id, "figure"),
        [Input(graph_id, "hoverData"), Input(graph_id, "clickData")],
    )
    def update_figure(hoverData, clickData):
        # Dupliquer pour ne jamais muter la figure d'origine
        fig = copy.deepcopy(base_figure)

        # Structure attendue: trace 0 (ligne), traces 1..5 (zones)
        if not getattr(fig, "data", None) or len(fig.data) < 6:
            return fig

        def extract_curve(data_event) -> Optional[int]:
            if not data_event or not data_event.get("points"):
                return None
            return data_event["points"][0].get("curveNumber")

        hover_curve = extract_curve(hoverData)
        click_curve = extract_curve(clickData)

        for idx in range(1, 6):
            fill = color_cfg.base
            if idx == hover_curve:
                fill = color_cfg.hover
            if idx == click_curve:
                fill = color_cfg.click

            trace = fig.data[idx]
            if hasattr(trace, "fillcolor"):
                trace.fillcolor = fill
            if hasattr(trace, "line"):
                trace.line.width = 0

        return fig

    @app.callback(Output(hover_output_id, "children"), Input(graph_id, "hoverData"))
    def hover_info(hoverData):
        if not hoverData or not hoverData.get("points"):
            return "Survolez une zone pour voir les détails."
        curve = hoverData["points"][0].get("curveNumber")
        return f"Vous survolez : {labels.get(curve, 'Zone inconnue')}"

    @app.callback(Output(click_output_id, "children"), Input(graph_id, "clickData"))
    def click_info(clickData):
        if not clickData or not clickData.get("points"):
            return "Cliquez sur une zone pour voir les détails."
        curve = clickData["points"][0].get("curveNumber")
        return f"Vous avez cliqué sur : {labels.get(curve, 'Zone inconnue')}"


__all__ = ["ZoneColors", "DEFAULT_ZONE_LABELS", "register_callbacks"]
