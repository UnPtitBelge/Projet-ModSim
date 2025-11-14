"""Sert d'exemple, à retirer après essai"""

import panel as pn
import numpy as np

from matplotlib.figure import Figure

ACCENT = "teal"
LOGO = "https://assets.holoviz.org/panel/tutorials/matplotlib-logo.png"

pn.extension(sizing_mode="stretch_width")

data = np.random.normal(1, 1, size=100)
fig = Figure(figsize=(8, 4))
ax = fig.subplots()
ax.hist(data, bins=15, color=ACCENT)

component = pn.pane.Matplotlib(fig, format='svg', sizing_mode='scale_both')

pn.template.FastListTemplate(
    title="My MatplotLib App", sidebar=[LOGO], main=[component], accent=ACCENT
).servable()
