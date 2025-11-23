import numpy as np
import panel as pn
from bokeh.models import ColumnDataSource, Range1d
from bokeh.plotting import figure

from src.app.classifier import Classifier
from src.app.models import AppConfig


class PoinCarePlot:
    def __init__(self, config: AppConfig, classifier: Classifier, regions=None) -> None:
        self.config = config
        self.classifier = classifier
        self.regions = regions if regions is not None else []
        self.source = ColumnDataSource(data=dict(x=[0.0], y=[0.0]))
        self.md = pn.pane.Markdown("", sizing_mode="stretch_width")
        self._build_figure()

    def _build_figure(self) -> None:
        self.fig = figure(
            title="Poincaré Diagram (Tr A vs det A)",
            x_range=Range1d(self.config.tr_min, self.config.tr_max),
            y_range=Range1d(self.config.det_min, self.config.det_max),
            tools="pan,wheel_zoom,box_zoom,reset,save,tap",
            sizing_mode="stretch_both",
        )
        # draw axes, lines patches, regions, ...
        self.fig.line(
            np.linspace(self.config.tr_min, self.config.tr_max, 500),
            (np.linspace(self.config.tr_min, self.config.tr_max, 500) ** 2) / 4.0,
            line_width=3,
            line_color="#ff9900",
            legend_label="Δ = 0 (det = (Tr)^2 / 4)",
        )

    def move_point(self, x, y):
        # clamp to config bounds
        x = max(self.config.tr_min, min(self.config.tr_max, x))
        y = max(self.config.det_min, min(self.config.det_max, y))
        self.source.data = dict(x=[x], y=[y])
        result = self.classifier.classify(x, y)
        self.md.object = f"**Current position**: (Tr A = {x:.3g}, det A = {y:.3g})\n\n{result.markdown}"

    def register_events(self):
        from bokeh.events import Tap

        def on_tap(event):
            self.move_point(event.x, event.y)

        self.fig.on_event(Tap, on_tap)

    def render_template(self):
        return pn.Column(self.fig, self.md)
