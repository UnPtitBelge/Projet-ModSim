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


# Labels par défaut (français) — par indices (fallback)
DEFAULT_ZONE_LABELS: Dict[int, str] = {
    1: "Foyer stable",
    2: "Foyer instable",
    3: "Noeud stable",
    4: "Noeud instable",
    5: "Selle",
    6: "Noeud stable dégénéré",
    7: "Noeud instable dégénéré",
    8: "Centre",
    9: "Ligne de points d'équilibre stable",
    10: "Ligne de points d'équilibre instable",
    11: "Mouvement uniforme",
}

# Labels par meta — robuste aux changements d'indices
LABEL_BY_META: Dict[str, str] = {
    # Zones
    "ulp": "Foyer stable",
    "urp": "Foyer instable",
    "llp": "Noeud stable",
    "lrp": "Noeud instable",
    "lxa": "Selle",
    # Parabole (parts)
    "parabola_left": "Parabole (partie gauche) → Noeud stable dégénéré",
    "parabola_right": "Parabole (partie droite) → Noeud instable dégénéré",
    # Axes
    "y": "Centre",
    "x_left": "Droite en x (partie gauche) → Ligne de points d'équilibre stable",
    "x_right": "Droite en x (partie droite) → Ligne de points d'équilibre instable",
    # Origine
    "origin": "Origine (τ=0, Δ=0) → Mouvement uniforme",
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

        # Coloriser uniquement les zones (par meta), pas les axes/parabole/point
        for idx, trace in enumerate(fig_any.data):
            meta = getattr(trace, "meta", None)
            state = "base"

            # Déterminer l'état (base / hover / click) pour cette trace
            if hover_curve == idx:
                state = "hover"
            if click_curve == idx:
                state = "click"

            # 1) Zones (polygones) — meta: ulp, urp, llp, lrp, lxa
            if meta in {"ulp", "urp", "llp", "lrp", "lxa"}:
                fill = color_cfg.base
                if state == "hover":
                    fill = color_cfg.hover
                if state == "click":
                    fill = color_cfg.click
                log.debug(
                    "Colorisation zone index=%d meta=%s état=%s couleur=%s",
                    idx,
                    meta,
                    state,
                    fill,
                )
                if hasattr(trace, "fillcolor"):
                    trace.fillcolor = fill
                # Masquer les bordures pour rester homogène
                line_obj = getattr(trace, "line", None)
                if line_obj is not None and hasattr(line_obj, "width"):
                    try:
                        line_obj.width = 0
                    except Exception:
                        pass
                continue

            # 2) Lignes (parabole gauche/droite, axes x/y) — accentuer sur hover/click
            if meta in {"parabola_left", "parabola_right", "y", "x_left", "x_right"}:
                line_obj = getattr(trace, "line", None)
                marker_obj = getattr(trace, "marker", None)
                if line_obj is not None or marker_obj is not None:
                    try:
                        # Accentuer largeur et couleur des lignes, et taille/couleur des marqueurs selon l'état
                        if state == "hover":
                            if line_obj is not None:
                                line_obj.width = 8
                                if hasattr(line_obj, "color"):
                                    line_obj.color = color_cfg.hover
                            if marker_obj is not None:
                                base_size = getattr(marker_obj, "size", None) or 6
                                marker_obj.size = max(base_size, 9)
                                # Harmoniser la couleur du marqueur avec l'état
                                marker_obj.color = color_cfg.hover
                        elif state == "click":
                            if line_obj is not None:
                                line_obj.width = 10
                                if hasattr(line_obj, "color"):
                                    line_obj.color = color_cfg.click
                            if marker_obj is not None:
                                base_size = getattr(marker_obj, "size", None) or 6
                                marker_obj.size = max(base_size, 11)
                                marker_obj.color = color_cfg.click
                        else:
                            # État de base: conserver les valeurs existantes (ligne et marqueur)
                            pass
                        log.debug("Accentuation ligne/markers index=%d meta=%s état=%s", idx, meta, state)
                    except Exception:
                        pass
                continue

            # 3) Point à l'origine — accentuer taille/bordure sur hover/click
            if meta == "origin":
                marker_obj = getattr(trace, "marker", None)
                if marker_obj is not None:
                    try:
                        base_size = getattr(marker_obj, "size", None) or 10
                        base_line = getattr(marker_obj, "line", None)
                        # Initialiser la ligne si absente
                        if base_line is None:
                            marker_obj.line = dict(width=0, color=color_cfg.base)
                            base_line = marker_obj.line
                        if state == "hover":
                            marker_obj.size = max(base_size, 16)
                            base_line["width"] = 3
                            base_line["color"] = color_cfg.hover
                        elif state == "click":
                            marker_obj.size = max(base_size, 20)
                            base_line["width"] = 5
                            base_line["color"] = color_cfg.click
                        else:
                            # État de base: laisser les valeurs existantes
                            pass
                        log.debug("Accentuation point origine index=%d état=%s", idx, state)
                    except Exception:
                        pass
                continue

        return fig_any

    # Navigation serveur réintroduite : la redirection est gérée par une callback
    # mettant à jour dcc.Location (id="url") pour déclencher le rendu multipage.
    @app.callback(Output("url", "pathname"), Input(graph_id, "clickData"))
    def navigate_on_click(clickData):
        """
        Navigation multipage déclenchée sur clic: zones, parabole gauche/droite, axes x/y et origine.
        """
        if not clickData or not clickData.get("points"):
            return no_update
        pt = clickData["points"][0]
        curve = pt.get("curveNumber")
        # Tentative par meta (robuste)
        try:
            meta = getattr(base_figure.data[curve], "meta", None)
        except Exception:
            meta = None
        if meta is not None:
            target = PATH_BY_META.get(str(meta))
            if target:
                log.info("Navigation via meta=%s vers %s (curve=%d)", meta, target, curve)
                return target
        # Fallback par index
        target = ZONE_PATH_MAP.get(curve)
        if target:
            log.info("Navigation via index vers %s (curve=%d)", target, curve)
            return target
        log.debug("Clic sans route associée (curve=%s meta=%s).", curve, meta)
        return no_update

    @app.callback(Output(hover_output_id, "children"), Input(graph_id, "hoverData"))
    def hover_info(hoverData):
        if not hoverData or not hoverData.get("points"):
            log.debug("Hover sorti de zone ou vide.")
            return "Survolez une zone pour voir les détails."
        pt = hoverData["points"][0]
        curve = pt.get("curveNumber")
        # Essayer de récupérer le meta de la trace pour une identification robuste
        meta = None
        try:
            meta = app._callback_list and app  # placeholder to avoid static check
        except Exception:
            meta = None
        # Récupérer le meta depuis la figure de base (plus fiable)
        try:
            meta = getattr(base_figure.data[curve], "meta", None)
        except Exception:
            meta = None
        label = LABEL_BY_META.get(str(meta)) if meta is not None else None
        label = label or labels.get(curve, "Zone inconnue")
        log.debug("Hover sur curve=%s meta=%s label=%s", curve, meta, label)
        return f"Vous survolez : {label}"

    @app.callback(Output(click_output_id, "children"), Input(graph_id, "clickData"))
    def click_info(clickData):
        if not clickData or not clickData.get("points"):
            log.debug("Clic hors zone ou vide.")
            return "Cliquez sur une zone pour voir les détails."
        pt = clickData["points"][0]
        curve = pt.get("curveNumber")
        try:
            meta = getattr(base_figure.data[curve], "meta", None)
        except Exception:
            meta = None
        label = LABEL_BY_META.get(str(meta)) if meta is not None else None
        label = label or labels.get(curve, "Zone inconnue")
        log.info("Clic sur curve=%s meta=%s label=%s", curve, meta, label)
        return f"Vous avez cliqué sur : {label}"


# Mapping curveNumber -> pathname (sans accents) pour navigation vers pages de stabilité
ZONE_PATH_MAP: Dict[int, str] = {
    1: "/stabilite/foyer_stable",
    2: "/stabilite/foyer_instable",
    3: "/stabilite/noeud_stable",
    4: "/stabilite/noeud_instable",
    5: "/stabilite/selle",
    # Fallbacks si indices utilisés pour axes/parabole/point (à ajuster selon figure)
    6: "/stabilite/noeud_stable_degenere",     # parabole gauche (exemple)
    7: "/stabilite/noeud_instable_degenere",   # parabole droite (exemple)
    8: "/stabilite/centre",                    # y line (centre)
    9: "/stabilite/ligne_pe_stable",           # x left
    10: "/stabilite/ligne_pe_instable",        # x right
    11: "/stabilite/mouvement_uniforme",       # origin
}

# Mapping par meta — navigation robuste
PATH_BY_META: Dict[str, str] = {
    "ulp": "/stabilite/foyer_stable",
    "urp": "/stabilite/foyer_instable",
    "llp": "/stabilite/noeud_stable",
    "lrp": "/stabilite/noeud_instable",
    "lxa": "/stabilite/selle",
    "parabola_left": "/stabilite/noeud_stable_degenere",
    "parabola_right": "/stabilite/noeud_instable_degenere",
    "y": "/stabilite/centre",
    "x_left": "/stabilite/ligne_pe_stable",
    "x_right": "/stabilite/ligne_pe_instable",
    "origin": "/stabilite/mouvement_uniforme",
}


# Ancienne fonction de navigation séparée supprimée (intégrée dans update_figure_and_navigate)


__all__ = [
    "ZoneColors",
    "DEFAULT_ZONE_LABELS",
    "register_callbacks",
]
