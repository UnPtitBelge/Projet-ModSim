"""
Construit la figure Plotly du diagramme de Poincaré afin de reproduire fidèlement
la figure de `src/temp/poincare_temp.py`:
- 5 zones (polygones) aux mêmes formes et couleurs
- Parabole et axes tracés avec les mêmes couleurs/épaisseurs
- Axes masqués et marges nulles

IMPORTANT (indices de traces attendus par les callbacks):
0  parabole (ligne) — conservé pour compatibilité avec callbacks existants
1  zone supérieure gauche
2  zone supérieure droite
3  zone inférieure gauche
4  zone inférieure droite
5  zone sous l'axe x
6+ éléments décoratifs additionnels (axes, parabole en surcouche) — ignorés par les callbacks

API principale: build_poincare_figure(config=None) -> plotly.graph_objs.Figure
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import plotly.graph_objs as go

from .constants import N_SAMPLES, TAU_MAX, TAU_MIN


@dataclass(frozen=True)
class PoincareConfig:
    # Domaine échantillonné
    tau_min: float = TAU_MIN
    tau_max: float = TAU_MAX
    samples: int = N_SAMPLES

    # Styles (adaptés à poincare_temp.py)
    line_width: int = 6
    main_line_color: str = "rgba(100,149,237,0.9)"  # CornflowerBlue
    # Couleurs des zones
    color_upper_left: str = "rgba(255,165,0,0.3)"  # orange pastel
    color_upper_right: str = "rgba(0,191,255,0.3)"  # bleu ciel transparent
    color_lower_left: str = "rgba(255,182,193,0.4)"  # rose pastel
    color_lower_right: str = "rgba(100,149,237,0.2)"  # bleu pastel
    color_lower_axis: str = "rgba(211,211,211,0.5)"  # gris pastel
    # Mise en page
    plot_bgcolor: str = "white"


def _core_arrays(cfg: PoincareConfig):
    """
    Génére le vecteur tau et la parabole.
    """
    tau_vals = np.linspace(cfg.tau_min, cfg.tau_max, cfg.samples)
    parabola_vals = (tau_vals**2) / 4.0
    return tau_vals, parabola_vals


def build_poincare_figure(config: PoincareConfig | None = None) -> go.Figure:
    """
    Construit et retourne la figure Poincaré mimant `src/temp/poincare_temp.py`
    tout en préservant les indices 0..5 attendus par les callbacks.
    """
    cfg = config or PoincareConfig()

    # Données de base
    x, y_parab = _core_arrays(cfg)
    # Découpage gauche/droite (inclut 0 des deux côtés si présent)
    x_left = x[x <= 0]
    y_left = y_parab[x <= 0]
    x_right = x[x >= 0]
    y_right = y_parab[x >= 0]

    # Étendue symétrique des axes comme dans le temp (val_max)
    val_max = max(abs(cfg.tau_min), abs(cfg.tau_max))

    fig = go.Figure()

    # 0. Parabole (INDEX 0 requis par les callbacks)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_parab,
            mode="lines",
            line=dict(color=cfg.main_line_color, width=cfg.line_width),
            name="parabola line",
            meta="parabola",
            hoverinfo="none",
            showlegend=False,
        )
    )

    # Helper pour les zones
    def add_zone(zone_x, zone_y, fillcolor, name, meta):
        fig.add_trace(
            go.Scatter(
                x=zone_x,
                y=zone_y,
                mode="lines+markers",
                fill="toself",
                fillcolor=fillcolor,
                line=dict(color="rgba(0,0,0,0)"),
                name=name,
                meta=meta,
                hoverinfo="none",
                hoveron="points+fills",
                showlegend=False,
            )
        )

    # 1. Zone au-dessus de la parabole à gauche (polygone fermé)
    # x=0 → longe la parabole côté gauche (vers -val) → retour x=0
    ul_x = np.concatenate([[0.0], x_left[::-1], [0.0]])
    ul_y = np.concatenate([[0.0], y_left[::-1], [y_left[0] if len(y_left) else 0.0]])
    add_zone(ul_x, ul_y, cfg.color_upper_left, "upper left parabola", "ulp")

    # 2. Zone au-dessus de la parabole à droite
    # x=0 → longe la parabole côté droit → retour x=0
    ur_x = np.concatenate([[0.0], x_right, [0.0]])
    ur_y = np.concatenate([[0.0], y_right, [y_right[-1] if len(y_right) else 0.0]])
    add_zone(ur_x, ur_y, cfg.color_upper_right, "upper right parabola", "urp")

    # 3. Zone sous la parabole à gauche (de -val_max à 0)
    ll_x = np.concatenate([[-val_max], x_left, [0.0]])
    ll_y = np.concatenate([[y_left[-1] if len(y_left) else 0.0], y_left, [0.0]])
    add_zone(ll_x, ll_y, cfg.color_lower_left, "lower left parabola", "llp")

    # 4. Zone sous la parabole à droite (de 0 à +val_max)
    lr_x = np.concatenate([[0.0], x_right, [val_max]])
    lr_y = np.concatenate([[y_right[0] if len(y_right) else 0.0], y_right, [0.0]])
    add_zone(lr_x, lr_y, cfg.color_lower_right, "lower right parabola", "lrp")

    # 5. Zone sous l'axe x (rectangle plein)
    lxa_x = [-val_max, val_max, val_max, -val_max]
    lxa_y = [0.0, 0.0, -val_max, -val_max]
    add_zone(lxa_x, lxa_y, cfg.color_lower_axis, "lower x axis", "lxa")

    # Traces décoratives (indices >= 6) — pour reproduire l'apparence exacte:
    # Axe vertical (y)
    fig.add_trace(
        go.Scatter(
            x=[0.0, 0.0],
            y=[0.0, val_max],
            mode="lines",
            line=dict(color=cfg.main_line_color, width=cfg.line_width),
            name="y line",
            meta="y",
            hoverinfo="none",
            showlegend=False,
        )
    )
    # Axe horizontal (x)
    fig.add_trace(
        go.Scatter(
            x=[-val_max, val_max],
            y=[0.0, 0.0],
            mode="lines",
            line=dict(color=cfg.main_line_color, width=cfg.line_width),
            name="x line",
            meta="x",
            hoverinfo="none",
            showlegend=False,
        )
    )
    # Parabole en surcouche pour la lisibilité (même style que l'index 0)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_parab,
            mode="lines",
            line=dict(color=cfg.main_line_color, width=cfg.line_width),
            name="parabola overlay",
            meta="parabola_top",
            hoverinfo="none",
            showlegend=False,
        )
    )

    # Layout identique au temp: axes masqués, fond blanc, marges nulles, bornes [-val_max, val_max]
    fig.update_layout(
        xaxis=dict(
            showgrid=False, zeroline=False, visible=False, range=[-val_max, val_max]
        ),
        yaxis=dict(
            showgrid=False, zeroline=False, visible=False, range=[-val_max, val_max]
        ),
        plot_bgcolor=cfg.plot_bgcolor,
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="closest",
    )

    return fig


_cached_figure: go.Figure | None = None


def get_cached_poincare_figure(config: PoincareConfig | None = None) -> go.Figure:
    """
    Retourne une figure Poincaré mise en cache.
    - Première invocation: construit et stocke la figure.
    - Si un config non None est passé: reconstruit avec cette config et met à jour le cache.
    - Appels suivants sans config: réutilisent la figure existante.
    """
    global _cached_figure
    if _cached_figure is None or config is not None:
        _cached_figure = build_poincare_figure(config)
    return _cached_figure


__all__ = ["PoincareConfig", "build_poincare_figure", "get_cached_poincare_figure"]
