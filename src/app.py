import numpy as np
import panel as pn
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Span, Label
from bokeh.events import Tap

pn.extension(sizing_mode="stretch_width")

# --- Parameters / grid
TR_MIN, TR_MAX = -10, 10
DET_MIN, DET_MAX = -10, 30
tr = np.linspace(TR_MIN, TR_MAX, 800)
det_curve = tr**2 / 4.0

# --- Bokeh figure
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,tap"
p = figure(
    title="Diagramme de Poincaré (Tr A vs det A) — cliquez pour déplacer le point",
    x_range=(TR_MIN, TR_MAX),
    y_range=(DET_MIN, DET_MAX),
    tools=TOOLS,
    sizing_mode="stretch_both"
)

# parabola Δ = 0 : det = (Tr)^2 / 4
p.line(tr, det_curve, line_width=3, line_color="#ff9900", legend_label="Δ = 0 (det = (Tr)^2 / 4)")

# Fill regions above (Δ > 0) and below (Δ < 0)
p.patch(
    np.concatenate([tr, tr[::-1]]),
    np.concatenate([det_curve, np.full_like(det_curve, DET_MAX)]),
    fill_alpha=0.08, fill_color="#fff0d9", line_color=None
)
p.patch(
    np.concatenate([tr, tr[::-1]]),
    np.concatenate([det_curve, np.full_like(det_curve, DET_MIN)]),
    fill_alpha=0.08, fill_color="#e8f6ff", line_color=None
)

# Axes lines
p.add_layout(Span(location=0, dimension='width',  line_color='black', line_width=1))
p.add_layout(Span(location=0, dimension='height', line_color='black', line_width=1))

p.xaxis.axis_label = "Tr A"
p.yaxis.axis_label = "det A"

# --- Movable point
source = ColumnDataSource(data=dict(x=[0.0], y=[0.0]))
p.square('x', 'y', size=12, fill_color="white", line_color="black", source=source)

# ------------------------------------------------------------------
# CLASSIFICATION LOGIC
# ------------------------------------------------------------------

md = pn.pane.Markdown("", sizing_mode="stretch_width")

def classify(trval, detval):
    Delta = trval**2 - 4*detval

    # Saddle
    if detval < 0:
        return f"**Selle (saddle)** — det < 0\nΔ = {Delta:.3g} < 0"

    # Degenerate (Δ = 0)
    if abs(Delta) < 1e-8:
        if trval == 0 and detval == 0:
            return "Origine dégénérée (0,0)"
        stability = "stable" if trval < 0 else "instable"
        return f"**Nœud dégénéré ({stability})** — Δ = 0"

    # Complex eigenvalues (spirals or center)
    if Delta < 0:
        if abs(trval) < 1e-8:
            return f"**Centre** — Tr A ≈ 0, Δ < 0"
        stability = "stable (spiral sink)" if trval < 0 else "instable (spiral source)"
        return f"**{stability}** — Δ < 0"

    # Δ > 0 & det > 0 → node (real eigenvalues)
    stability = "stable (node sink)" if trval < 0 else "instable (node source)"
    return f"**{stability}** — Δ > 0"

# initial text
md.object = f"**Position courante**: TrA = 0.000, detA = 0.000\n\n{classify(0.0, 0.0)}"

# ------------------------------------------------------------------
# CLICK EVENT
# ------------------------------------------------------------------
def on_tap(event):
    x = max(min(event.x, TR_MAX), TR_MIN)
    y = max(min(event.y, DET_MAX), DET_MIN)

    source.data = dict(x=[x], y=[y])
    md.object = (
        f"**Position courante**: TrA = {x:.3f}, detA = {y:.3f}\n\n{classify(x, y)}"
    )

p.on_event(Tap, on_tap)

# region labels
labels = [
    Label(x=0, y=22, text="Spirales / Nœuds\n(Δ > 0)", text_align='center'),
    Label(x=0, y=-4, text="Selle\n(Δ < 0)", text_align='center'),
    Label(x=0, y=1.0, text="Zone centre possible\n(Tr A = 0, Δ < 0)", text_align='center')
]
for lab in labels:
    p.add_layout(lab)

p.legend.location = "top_left"

# ------------------------------------------------------------------
# PANEL TEMPLATE (dark)
# ------------------------------------------------------------------

template = pn.template.FastListTemplate(
    title="Projet ModSim — Analyse de stabilité",
    theme="dark",
    sidebar=[
        pn.pane.Markdown(
            "### Instructions\n"
            "- Cliquez sur le graphique pour déplacer le point.\n"
            "- La classification du point s'affiche automatiquement.\n"
        )
    ],
    main=[p, pn.layout.Divider(), md],
    accent_base_color="#ff9900"
)

template.servable()
