"""Main application module for the stability analysis visualization tool.

This module builds a Panel + Bokeh interactive Poincaré diagram (Tr A vs det A)
that allows the user to click to move a point and see the stability classification
of the corresponding 2x2 linear system.

Dependencies: numpy, panel, bokeh
Exposes: `template.servable()` when run as a Panel app
"""

import panel as pn

import show, config

pn.extension(sizing_mode="stretch_width")

from classifier import classify


# Build the UI template using the plotting module and the classify callback
template = show.build_template(classify)


if __name__.startswith("__main__"):
    # Make the app servable when run as a script
    template.servable()
else:
    # When imported by Panel server, register the template
    template.servable()
