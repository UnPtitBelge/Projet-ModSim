import numpy as np
import panel as pn
from bokeh.models import ColumnDataSource, Label, Range1d, Span
from bokeh.plotting import figure
from models import AppConfig


class PoincarePlot:
    """Construct the Poincaré diagram UI and expose a Panel template.

    This class centralizes the plotting and UI wiring previously in `show.py`.
    It expects `classifier` to be an object with a `classify(tr, det)` method
    (or a callable adapter providing the same).
    """

    def __init__(self, config: AppConfig, classifier, regions=None) -> None:
        self.config = config
        self.classifier = classifier
        self.regions = regions if regions is not None else []
        self.source = ColumnDataSource(data=dict(x=[0.0], y=[0.0]))
        self.md = pn.pane.Markdown("", sizing_mode="stretch_width")
        self._build_figure()

    def _build_figure(self) -> None:
        self.fig = figure(
            title="Poincaré Diagram (Tr A vs det A) — click to move the point",
            x_range=Range1d(self.config.tr_min, self.config.tr_max),
            y_range=Range1d(self.config.det_min, self.config.det_max),
            tools="pan,wheel_zoom,box_zoom,reset,save,tap",
            sizing_mode="stretch_both",
        )

        # Prepare grid and curve
        tr_vals = np.linspace(
            self.config.tr_min, self.config.tr_max, self.config.grid_res
        )
        det_curve = tr_vals**2 / 4.0

        # main parabola line
        self.fig.line(
            tr_vals,
            det_curve,
            line_width=3,
            line_color="#ff9900",
            legend_label="Δ = 0 (det = (Tr)^2 / 4)",
        )

        # axis dashed lines
        self.fig.line(
            tr_vals,
            np.full_like(tr_vals, 0),
            line_width=2,
            line_color="#00aaff",
            line_dash="dashed",
            legend_label="y = 0",
        )
        self.fig.line(
            np.full(2, 0.0),
            np.linspace(self.config.det_min, self.config.det_max, 2),
            line_width=2,
            line_color="#00aaff",
            line_dash="dashed",
            legend_label="x = 0",
        )

        # Fill regions (above and below parabola)
        self.fig.patch(
            np.concatenate([tr_vals, tr_vals[::-1]]),
            np.concatenate([det_curve, np.full_like(det_curve, self.config.det_max)]),
            fill_alpha=0.08,
            fill_color="#fff0d9",
            line_color=None,
        )
        self.fig.patch(
            np.concatenate([tr_vals, tr_vals[::-1]]),
            np.concatenate([det_curve, np.full_like(det_curve, self.config.det_min)]),
            fill_alpha=0.08,
            fill_color="#e8f6ff",
            line_color=None,
        )

        # Axes lines and labels
        self.fig.add_layout(
            Span(location=0, dimension="width", line_color="black", line_width=1)
        )
        self.fig.add_layout(
            Span(location=0, dimension="height", line_color="black", line_width=1)
        )
        self.fig.xaxis.axis_label = "Tr A"
        self.fig.yaxis.axis_label = "det A"

        # Movable point
        self.fig.scatter(
            "x",
            "y",
            size=12,
            marker="square",
            fill_color="white",
            line_color="black",
            source=self.source,
        )

        # initial text using classifier (supports both structured result or string)
        initial = self.classifier.classify(0.0, 0.0)
        md_text = getattr(initial, "markdown", str(initial))
        self.md.object = f"**Current position**: TrA = 0.000, detA = 0.000\n\n{md_text}"

        # Click event handler uses provided classifier
        def _on_tap(event):
            x = max(min(event.x, self.config.tr_max), self.config.tr_min)
            y = max(min(event.y, self.config.det_max), self.config.det_min)

            self.source.data = dict(x=[x], y=[y])
            out = self.classifier.classify(x, y)
            md_text = getattr(out, "markdown", str(out))
            self.md.object = (
                f"**Current position**: TrA = {x:.3f}, detA = {y:.3f}\n\n{md_text}"
            )

        # register handler
        self.fig.on_event("tap", _on_tap)

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
            self.fig.add_layout(lab)

        self.fig.legend.location = "top_left"

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
            main=[self.fig, pn.layout.Divider(), self.md],
            accent_base_color="#ff9900",
        )

        # store for access
        self._template = template

    def move_point(self, x, y):
        # clamp to config bounds
        x = max(self.config.tr_min, min(self.config.tr_max, x))
        y = max(self.config.det_min, min(self.config.det_max, y))
        self.source.data = dict(x=[x], y=[y])
        result = self.classifier.classify(x, y)
        md_text = getattr(result, "markdown", str(result))
        self.md.object = (
            f"**Current position**: (Tr A = {x:.3g}, det A = {y:.3g})\n\n{md_text}"
        )

    def register_events(self):
        # kept for compatibility; events are already registered in _build_figure
        pass

    def render_template(self):
        return self._template
