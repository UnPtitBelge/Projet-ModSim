"""Main application module for the stability analysis visualization tool.

This module builds a Panel + Bokeh interactive Poincaré diagram (Tr A vs det A)
that allows the user to click to move a point and see the stability classification
of the corresponding 2x2 linear system.

Dependencies: numpy, panel, bokeh
Exposes: `template.servable()` when run as a Panel app
"""

import panel as pn

from .classifier import Classifier
from .show import *

pn.extension(sizing_mode="stretch_width")

# Build the UI template using the plotting module and the classify callback
template = build_template(Classifier().classify)


if __name__.startswith("__main__"):
    # Make the app servable when run as a script
    template.servable()
else:
    # When imported by Panel server, register the template
    template.servable()
