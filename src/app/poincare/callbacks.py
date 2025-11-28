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
    Graph        : "poincare-graph"
    Survol texte : "output-temp-hover"
    Clic texte   : "output-temp-click"
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Dict, Optional

import plotly.graph_objs as go
from dash import Dash, Input, Output, no_update  # type: ignore

from src.app.logging_setup import get_logger


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
    graph_id: str = "poincare-graph",
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
    log = get_logger(__name__)
    log.debug(
        "Initialisation des callbacks Poincaré (graph_id=%s, hover_output_id=%s, click_output_id=%s)",
        graph_id,
        hover_output_id,
        click_output_id,
    )
    color_cfg = colors or ZoneColors()
    labels = zone_labels or DEFAULT_ZONE_LABELS
    log.debug(
        "Configuration des couleurs: base=%s hover=%s click=%s",
        color_cfg.base,
        color_cfg.hover,
        color_cfg.click,
    )

    @app.callback(
        Output(graph_id, "figure"),
        [Input(graph_id, "hoverData"), Input(graph_id, "clickData")],
    )
    def update_figure(hoverData, clickData):
        """
        Met à jour uniquement la figure (couleurs hover / click).
        Navigation séparée pour éviter toute interaction de rendu.
        """
        log.debug(
            "Interaction reçue (hoverData=%s, clickData=%s)",
            bool(hoverData),
            bool(clickData),
        )
        fig_any: Any = copy.deepcopy(base_figure)
        try:
            _ = fig_any.data[5]  # Vérifie la présence des zones
        except Exception:
            log.warning("Figure inattendue: moins de 6 traces (coloration uniquement).")
            return fig_any

        def extract_curve(data_event) -> Optional[int]:
            if not data_event or not data_event.get("points"):
                return None
            return data_event["points"][0].get("curveNumber")

        hover_curve = extract_curve(hoverData)
        click_curve = extract_curve(clickData)
        log.debug("Indices détectés: hover=%s click=%s", hover_curve, click_curve)

        for idx in range(1, 6):
            fill = color_cfg.base
            state = "base"
            if idx == hover_curve:
                fill = color_cfg.hover
                state = "hover"
            if idx == click_curve:
                fill = color_cfg.click
                state = "click"
            log.debug(
                "Application couleur zone index=%d état=%s couleur=%s", idx, state, fill
            )

            trace: Any = fig_any.data[idx]
            if hasattr(trace, "fillcolor"):
                trace.fillcolor = fill
            line_obj = getattr(trace, "line", None)
            if line_obj is not None and hasattr(line_obj, "width"):
                try:
                    line_obj.width = 0
                except Exception:
                    pass

        return fig_any

    # Navigation serveur réintroduite : la redirection est gérée par une callback
    # mettant à jour dcc.Location (id="url") pour déclencher le rendu multipage.
    @app.callback(Output("url", "pathname"), Input(graph_id, "clickData"))
    def navigate_on_click(clickData):
        """
        Navigation multipage déclenchée uniquement sur clic (zones 1..5).
        """
        if not clickData or not clickData.get("points"):
            return no_update
        curve = clickData["points"][0].get("curveNumber")
        target = ZONE_PATH_MAP.get(curve)
        if target:
            log.info("Navigation déclenchée vers %s (zone index=%d)", target, curve)
            return target
        log.debug("Clic sans route associée (curve=%s).", curve)
        return no_update

    @app.callback(Output(hover_output_id, "children"), Input(graph_id, "hoverData"))
    def hover_info(hoverData):
        if not hoverData or not hoverData.get("points"):
            log.debug("Hover sorti de zone ou vide.")
            return "Survolez une zone pour voir les détails."
        curve = hoverData["points"][0].get("curveNumber")
        log.debug("Hover sur zone curveNumber=%s", curve)
        return f"Vous survolez : {labels.get(curve, 'Zone inconnue')}"

    @app.callback(Output(click_output_id, "children"), Input(graph_id, "clickData"))
    def click_info(clickData):
        if not clickData or not clickData.get("points"):
            log.debug("Clic hors zone ou vide.")
            return "Cliquez sur une zone pour voir les détails."
        curve = clickData["points"][0].get("curveNumber")
        log.info(
            "Clic sur zone curveNumber=%s label=%s",
            curve,
            labels.get(curve, "Inconnue"),
        )
        return f"Vous avez cliqué sur : {labels.get(curve, 'Zone inconnue')}"


# Mapping curveNumber -> pathname (sans accents) pour navigation vers pages de stabilité
ZONE_PATH_MAP: Dict[int, str] = {
    1: "/stabilite/zone-superieure-gauche",
    2: "/stabilite/zone-superieure-droite",
    3: "/stabilite/zone-inferieure-gauche",
    4: "/stabilite/zone-inferieure-droite",
    5: "/stabilite/zone-sous-axe-x",
}


# Ancienne fonction de navigation séparée supprimée (intégrée dans update_figure_and_navigate)


__all__ = [
    "ZoneColors",
    "DEFAULT_ZONE_LABELS",
    "register_callbacks",
]
