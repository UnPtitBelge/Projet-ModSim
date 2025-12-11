"""
Figure Plotly du diagramme de Poincaré.

Indices de traces (pour callbacks):
0: parabole (ligne)
1: foyer stable
2: foyer instable
3: noeud stable
4: noeud instable
5: selle

API: build_poincare_figure(config=None) -> plotly.graph_objs.Figure
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import plotly.graph_objs as go

from src.app.logging_setup import get_logger
from src.app.style.palette import PALETTE
from src.app.style.plot.theme import FIGURE_THEME, apply_to_figure

from .constants import N_SAMPLES, TAU_MAX, TAU_MIN


@dataclass(frozen=True)
class PoincareConfig:
    # Domaine échantillonné
    tau_min: float = TAU_MIN
    tau_max: float = TAU_MAX
    samples: int = N_SAMPLES

    # Styles (palette centrale)
    line_width: int = 3
    origin_gap_ratio: float = 2.0 / max(N_SAMPLES, 1)


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
    log = get_logger(__name__)
    log.debug(
        "Construction figure Poincaré: tau_min=%s tau_max=%s samples=%s line_width=%s",
        cfg.tau_min,
        cfg.tau_max,
        cfg.samples,
        cfg.line_width,
    )

    # Données de base
    x, y_parab = _core_arrays(cfg)
    x_left = x[x < 0]
    y_left = y_parab[x < 0]
    x_right = x[x > 0]
    y_right = y_parab[x > 0]

    val_max = max(abs(cfg.tau_min), abs(cfg.tau_max))
    log.debug("val_max calculé=%s", val_max)
    gap = max(cfg.origin_gap_ratio * val_max, 0.0)

    fig = go.Figure()

    def add_zone(zone_x, zone_y, name, meta):
        # Choix explicite de la couleur depuis PALETTE
        if meta == "llp":
            fillcolor = PALETTE.stability_stable
        elif meta == "lxa":
            fillcolor = PALETTE.secondary
        else:
            fillcolor = PALETTE.primary
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
                hoverinfo="text",
                text=[name] * len(zone_x),
                hovertemplate="%{text}<br>τ=%{x:.3f}, Δ=%{y:.3f}<extra></extra>",
                hoveron="fills",
                showlegend=False,
            )
        )
        log.debug("Zone ajoutée: %s meta=%s couleur=%s", name, meta, fillcolor)

    ul_x = np.concatenate([[0.0], x_left[::-1], [0.0]])
    ul_y = np.concatenate([[0.0], y_left[::-1], [y_left[0] if len(y_left) else 0.0]])
    add_zone(ul_x, ul_y, "Foyer stable", "ulp")

    ur_x = np.concatenate([[0.0], x_right, [0.0]])
    ur_y = np.concatenate([[0.0], y_right, [y_right[-1] if len(y_right) else 0.0]])
    add_zone(ur_x, ur_y, "Foyer instable", "urp")

    ll_x = np.concatenate([[-val_max], x_left, [0.0]])
    ll_y = np.concatenate([[y_left[-1] if len(y_left) else 0.0], y_left, [0.0]])
    add_zone(ll_x, ll_y, "Noeud stable", "llp")

    lr_x = np.concatenate([[0.0], x_right, [val_max]])
    lr_y = np.concatenate([[y_right[0] if len(y_right) else 0.0], y_right, [0.0]])
    add_zone(lr_x, lr_y, "Noeud instable", "lrp")

    lxa_x = [-val_max, val_max, val_max, -val_max]
    lxa_y = [0.0, 0.0, -val_max, -val_max]
    add_zone(lxa_x, lxa_y, "Selle", "lxa")

    # Échantillonnage dense de la ligne Y pour améliorer hover/click
    y_line = np.linspace(gap, val_max, cfg.samples)
    x_line = np.zeros_like(y_line)
    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines+markers",
            marker=dict(size=6, color=PALETTE.secondary),
            line=dict(color=PALETTE.secondary, width=cfg.line_width),
            name="Droite en y (τ = 0)",
            meta="y",
            hoverinfo="text",
            text=["Centre"] * len(y_line),
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )
    log.debug("Trace axe Y (échantillonnée) ajoutée (index %d).", len(fig.data) - 1)

    # Échantillonnage dense de la ligne X (partie gauche) pour améliorer hover/click
    x_left_line = np.linspace(-val_max, -gap, cfg.samples)
    y_left_line = np.zeros_like(x_left_line)
    fig.add_trace(
        go.Scatter(
            x=x_left_line,
            y=y_left_line,
            mode="lines+markers",
            marker=dict(size=6, color=PALETTE.secondary),
            line=dict(color=PALETTE.secondary, width=cfg.line_width),
            name="Droite en x (partie gauche)",
            meta="x_left",
            hoverinfo="text",
            text=["Ligne de points d'équilibre stable"] * len(x_left_line),
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )

    # Échantillonnage dense de la ligne X (partie droite) pour améliorer hover/click
    x_right_line = np.linspace(gap, val_max, cfg.samples)
    y_right_line_const = np.zeros_like(x_right_line)
    fig.add_trace(
        go.Scatter(
            x=x_right_line,
            y=y_right_line_const,
            mode="lines+markers",
            marker=dict(size=6, color=PALETTE.secondary),
            line=dict(color=PALETTE.secondary, width=cfg.line_width),
            name="Droite en x (partie droite)",
            meta="x_right",
            hoverinfo="text",
            text=["Ligne de points d'équilibre instable"] * len(x_right_line),
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )

    log.debug("Trace axe X (échantillonnée) ajoutée (index %d).", len(fig.data) - 1)

    fig.add_trace(
        go.Scatter(
            x=x_left,
            y=y_left,
            mode="lines",
            line=dict(color=PALETTE.secondary, width=cfg.line_width),
            name="Parabole (partie gauche)",
            meta="parabola_left",
            hoverinfo="text",
            text=["Noeud stable dégénéré"] * len(x_left),
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x_right,
            y=y_right,
            mode="lines",
            line=dict(color=PALETTE.secondary, width=cfg.line_width),
            name="Parabole (partie droite)",
            meta="parabola_right",
            hoverinfo="text",
            text=["Noeud instable dégénéré"] * len(x_right),
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )
    log.debug("Trace parabole overlay ajoutée (index %d).", len(fig.data) - 1)

    fig.add_trace(
        go.Scatter(
            x=[0.0],
            y=[0.0],
            mode="markers",
            marker=dict(size=12, color=PALETTE.third),
            name="Mouvement uniforme",
            meta="origin",
            hoverinfo="text",
            text=["Mouvement uniforme"],
            hovertemplate="%{text}<extra></extra>",
            showlegend=False,
        )
    )

    fig.update_layout(
        xaxis=dict(
            showgrid=False, zeroline=False, visible=False, range=[-val_max, val_max]
        ),
        yaxis=dict(
            showgrid=False, zeroline=False, visible=False, range=[-val_max, val_max]
        ),
        plot_bgcolor=PALETTE.secondary,
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="closest",
    )
    # Appliquer le thème centralisé (couleurs, typos, etc.)
    apply_to_figure(fig)
    log.info("Figure Poincaré construite avec %d traces.", len(fig.data))
    return fig


_cached_figure: go.Figure | None = None


def get_cached_poincare_figure(config: PoincareConfig | None = None) -> go.Figure:
    """
    Retourne une figure Poincaré mise en cache.
    - Première invocation: construit et stocke la figure.
    - Si un config non None est passé: reconstruit avec cette config et met à jour le cache.
    - Appels suivants sans config: réutilisent la figure existante.
    Logging:
        DEBUG cache hit/miss et reconstruction
        INFO  après (re)construction avec nombre de traces
    """
    global _cached_figure
    log = get_logger(__name__)
    if _cached_figure is None:
        log.debug("Cache miss: construction de la figure Poincaré.")
        _cached_figure = build_poincare_figure(config)
        log.info(
            "Figure Poincaré construite et mise en cache (traces=%d).",
            len(_cached_figure.data),
        )
    elif config is not None:
        log.debug(
            "Reconstruction de la figure Poincaré avec configuration personnalisée."
        )
        _cached_figure = build_poincare_figure(config)
        log.info(
            "Figure Poincaré reconstruite et mise à jour (traces=%d).",
            len(_cached_figure.data),
        )
    else:
        log.debug("Cache hit: réutilisation de la figure Poincaré.")
    return _cached_figure


__all__ = ["PoincareConfig", "build_poincare_figure", "get_cached_poincare_figure"]
