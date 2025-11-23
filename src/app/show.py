"""Visualization helpers and components for the application.

This module builds the Bokeh figure and the Panel template used by the
application. The plotting logic is self-contained and accepts a
classification callback so the UI can remain decoupled from business logic.

Public API
----------
build_template(classify_func) -> pn.template.FastListTemplate
        Build and return a Panel template. `classify_func(tr, det)` is used to
        produce the classification text when the user interacts with the plot.
"""

from __future__ import annotations

import numpy as np
import panel as pn
from bokeh.events import Tap
from bokeh.models import ColumnDataSource, Label, Span
from bokeh.plotting import figure

from .models import AppConfig

__all__ = ["build_template"]


def build_template(classify_func):
    """Build the interactive Poincaré diagram and return a Panel template.

    Parameters
    ----------
    classify_func: Callable[[float, float], str]
            Function that takes (tr, det) and returns a Markdown string.
    """
    # Local import to satisfy type-checkers that expect Range objects
    from bokeh.models import Range1d

    # Prepare grid
    tr = np.linspace(AppConfig.tr_min, AppConfig.tr_max, AppConfig.grid_res)
    det_curve = tr**2 / 4.0
    x_equal_0 = np.linspace(AppConfig.det_min, AppConfig.det_max, 2)

    # Bokeh figure
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,tap"
    p = figure(
        title="Poincaré Diagram (Tr A vs det A) — click to move the point",
        x_range=Range1d(AppConfig.tr_min, AppConfig.tr_max),
        y_range=Range1d(AppConfig.det_min, AppConfig.det_max),
        tools=TOOLS,
        sizing_mode="stretch_both",
    )

    p.line(
        tr,
        det_curve,
        line_width=3,
        line_color="#ff9900",
        legend_label="Δ = 0 (det = (Tr)^2 / 4)",
    )

    p.line(
        tr,
        np.full_like(tr, 0),
        line_width=2,
        line_color="#00aaff",
        line_dash="dashed",
        legend_label="y = 0",
    )

    p.line(
        np.full_like(x_equal_0, 0),
        x_equal_0,
        line_width=2,
        line_color="#00aaff",
        line_dash="dashed",
        legend_label="x = 0",
    )

    # Fill regions
    p.patch(
        np.concatenate([tr, tr[::-1]]),
        np.concatenate([det_curve, np.full_like(det_curve, AppConfig.det_max)]),
        fill_alpha=0.08,
        fill_color="#fff0d9",
        line_color=None,
    )
    p.patch(
        np.concatenate([tr, tr[::-1]]),
        np.concatenate([det_curve, np.full_like(det_curve, AppConfig.det_min)]),
        fill_alpha=0.08,
        fill_color="#e8f6ff",
        line_color=None,
    )

    # Axes lines and labels
    p.add_layout(Span(location=0, dimension="width", line_color="black", line_width=1))
    p.add_layout(Span(location=0, dimension="height", line_color="black", line_width=1))
    p.xaxis.axis_label = "Tr A"
    p.yaxis.axis_label = "det A"

    # Movable point
    source = ColumnDataSource(data=dict(x=[0.0], y=[0.0]))
    p.square("x", "y", size=12, fill_color="white", line_color="black", source=source)

    # Markdown pane for classification text
    md = pn.pane.Markdown("", sizing_mode="stretch_width")

    # initial text
    md.object = (
        f"**Current position**: TrA = 0.000, detA = 0.000\n\n{classify_func(0.0, 0.0)}"
    )

    # Click event handler uses provided classify function
    def on_tap(event):
        x = max(min(event.x, AppConfig.tr_max), AppConfig.tr_min)
        y = max(min(event.y, AppConfig.det_max), AppConfig.det_min)

        source.data = dict(x=[x], y=[y])
        md.object = f"**Current position**: TrA = {x:.3f}, detA = {y:.3f}\n\n{classify_func(x, y)}"

    p.on_event(Tap, on_tap)

    # region labels
    labels = [
        Label(x=0, y=22, text="Spirals / Nodes\n(Δ > 0)", text_align="center"),
        Label(x=0, y=-4, text="Saddle\n(Δ < 0)", text_align="center"),
        Label(
            x=0,
            y=1.0,
            text="Possible center region\n(Tr A = 0, Δ < 0)",
            text_align="center",
        ),
    ]
    for lab in labels:
        p.add_layout(lab)

    p.legend.location = "top_left"

    # Panel template
    template = pn.template.FastListTemplate(
        title="Projet ModSim — Stability analysis",
        theme="dark",
        sidebar=[
            pn.pane.Markdown(
                "### Instructions\n"
                "- Click the plot to move the point.\n"
                "- The point classification updates automatically.\n"
            )
        ],
        main=[p, pn.layout.Divider(), md],
        accent_base_color="#ff9900",
    )

    return template
