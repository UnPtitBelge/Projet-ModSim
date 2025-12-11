"""
Poincaré diagram callbacks for interactivity (hover, click) and zone navigation.

This module manages user interactions with the Poincaré diagram:
1. Hover effects: highlights zones under the cursor
2. Click navigation: redirects to the corresponding stability page
3. Zone identification: maps diagram regions to equilibrium types

The Poincaré diagram plots τ (trace) vs Δ (determinant) to show stability regions.
Clicking a zone navigates to the detailed page for that equilibrium type.

Supported equilibrium types:
- Foyer stable/instable (spiral convergence/divergence)
- Nœud stable/instable (direct convergence/divergence)
- Selle (saddle point)
- Centre (periodic orbits)
- Dégénérés (special cases)
- Ligne de PE (linear families)
- Mouvement uniforme (constant motion)
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Dict, Optional

import plotly.graph_objs as go
from dash import Dash, Input, Output, html  # type: ignore

from src.app.logging_setup import get_logger
from src.app.stabilite.base_layout import build_stability_layout
from src.app.stabilite.centre import create_figure as fig_centre
from src.app.stabilite.centre import layout_pedagogic as layout_centre
from src.app.stabilite.foyer_instable import \
    create_figure as fig_foyer_instable
from src.app.stabilite.foyer_instable import \
    layout_pedagogic as layout_foyer_instable
from src.app.stabilite.foyer_stable import create_figure as fig_foyer_stable
from src.app.stabilite.foyer_stable import \
    layout_pedagogic as layout_foyer_stable
from src.app.stabilite.ligne_pe_instable import \
    create_figure as fig_lpe_instable
from src.app.stabilite.ligne_pe_instable import \
    layout_pedagogic as layout_lpe_instable
from src.app.stabilite.ligne_pe_stable import create_figure as fig_lpe_stable
from src.app.stabilite.ligne_pe_stable import \
    layout_pedagogic as layout_lpe_stable
from src.app.stabilite.mouvement_uniforme import \
    create_figure as fig_mouvement_uniforme
from src.app.stabilite.mouvement_uniforme import \
    layout_pedagogic as layout_mouvement_uniforme
from src.app.stabilite.noeud_instable import \
    create_figure as fig_noeud_instable
from src.app.stabilite.noeud_instable import \
    layout_pedagogic as layout_noeud_instable
from src.app.stabilite.noeud_instable_degenere import \
    create_figure as fig_noeud_instable_deg
from src.app.stabilite.noeud_instable_degenere import \
    layout_pedagogic as layout_noeud_instable_deg
from src.app.stabilite.noeud_stable import create_figure as fig_noeud_stable
from src.app.stabilite.noeud_stable import \
    layout_pedagogic as layout_noeud_stable
from src.app.stabilite.noeud_stable_degenere import \
    create_figure as fig_noeud_stable_deg
from src.app.stabilite.noeud_stable_degenere import \
    layout_pedagogic as layout_noeud_stable_deg
from src.app.stabilite.selle import create_figure as fig_selle
from src.app.stabilite.selle import layout_pedagogic as layout_selle
from src.app.style.text import TEXT


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
) -> None:
    """
    Attache les callbacks d'interaction (hover + click) sur la figure Poincaré.

    Paramètres:
        app            : instance Dash
        base_figure    : figure immuable (parabole + zones)
        colors         : configuration des couleurs (optionnel)
        zone_labels    : dictionnaire curveNumber -> label (optionnel)
        graph_id       : id du composant dcc.Graph
    """
    log = get_logger(__name__)
    log.debug(
        "Initialisation des callbacks Poincaré (graph_id=%s)",
        graph_id,
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
                        log.debug(
                            "Accentuation ligne/markers index=%d meta=%s état=%s",
                            idx,
                            meta,
                            state,
                        )
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
                        log.debug(
                            "Accentuation point origine index=%d état=%s", idx, state
                        )
                    except Exception:
                        pass
                continue

        return fig_any

    @app.callback(
        Output("poincare-stability-panel", "children"), Input(graph_id, "clickData")
    )
    def render_stability_layout(clickData):
        """Affiche le layout de stabilité correspondant sous le diagramme (sans navigation)."""
        if not clickData or not clickData.get("points"):
            return html.Div(
                "Cliquez sur une zone du diagramme pour afficher la fiche correspondante.",
                style={**TEXT["p"], "marginTop": "8px"},
            )
        pt = clickData["points"][0]
        curve = pt.get("curveNumber")
        try:
            meta = getattr(base_figure.data[curve], "meta", None)
        except Exception:
            meta = None

        layout_builder = LAYOUT_BY_META.get(str(meta))
        if layout_builder:
            return layout_builder()

        fallback = LAYOUT_BY_INDEX.get(curve)
        if fallback:
            return fallback()

        return html.Div("Zone inconnue ou non supportée.", style=TEXT["p"])


# Mapping vers layouts (affichage inline, pas de navigation)
LAYOUT_BY_META: Dict[str, Any] = {
    "ulp": lambda: build_stability_layout(
        "foyer_stable",
        layout_foyer_stable,
        tau=-2.0,
        delta=2.0,
        create_phase_fig=fig_foyer_stable,
    ),
    "urp": lambda: build_stability_layout(
        "foyer_instable",
        layout_foyer_instable,
        tau=2.0,
        delta=2.0,
        create_phase_fig=fig_foyer_instable,
    ),
    "llp": lambda: build_stability_layout(
        "noeud_stable",
        layout_noeud_stable,
        tau=-2.0,
        delta=2.0,
        create_phase_fig=fig_noeud_stable,
    ),
    "lrp": lambda: build_stability_layout(
        "noeud_instable",
        layout_noeud_instable,
        tau=2.0,
        delta=2.0,
        create_phase_fig=fig_noeud_instable,
    ),
    "lxa": lambda: build_stability_layout(
        "selle", layout_selle, tau=0.0, delta=-1.0, create_phase_fig=fig_selle
    ),
    "parabola_left": lambda: build_stability_layout(
        "noeud_stable_degenere",
        layout_noeud_stable_deg,
        tau=-2.0,
        delta=1.0,
        create_phase_fig=fig_noeud_stable_deg,
    ),
    "parabola_right": lambda: build_stability_layout(
        "noeud_instable_degenere",
        layout_noeud_instable_deg,
        tau=2.0,
        delta=1.0,
        create_phase_fig=fig_noeud_instable_deg,
    ),
    "y": lambda: build_stability_layout(
        "centre", layout_centre, tau=0.0, delta=1.0, create_phase_fig=fig_centre
    ),
    "x_left": lambda: build_stability_layout(
        "ligne_pe_stable",
        layout_lpe_stable,
        tau=-2.0,
        delta=0.0,
        create_phase_fig=fig_lpe_stable,
    ),
    "x_right": lambda: build_stability_layout(
        "ligne_pe_instable",
        layout_lpe_instable,
        tau=2.0,
        delta=0.0,
        create_phase_fig=fig_lpe_instable,
    ),
    "origin": lambda: build_stability_layout(
        "mouvement_uniforme",
        layout_mouvement_uniforme,
        tau=0.0,
        delta=0.0,
        create_phase_fig=fig_mouvement_uniforme,
    ),
}

LAYOUT_BY_INDEX: Dict[int, Any] = {
    1: LAYOUT_BY_META["ulp"],
    2: LAYOUT_BY_META["urp"],
    3: LAYOUT_BY_META["llp"],
    4: LAYOUT_BY_META["lrp"],
    5: LAYOUT_BY_META["lxa"],
    6: LAYOUT_BY_META["parabola_left"],
    7: LAYOUT_BY_META["parabola_right"],
    8: LAYOUT_BY_META["y"],
    9: LAYOUT_BY_META["x_left"],
    10: LAYOUT_BY_META["x_right"],
    11: LAYOUT_BY_META["origin"],
}


__all__ = [
    "ZoneColors",
    "DEFAULT_ZONE_LABELS",
    "register_callbacks",
]
