import dash
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, dcc, html

app = dash.Dash(__name__)

x = np.linspace(-15, 15, 300)
y_parab = x**2 / 4
val_max = 15
line_width = 6

fig = go.Figure()

# -------------------------
x_left = x[x <= 0]
y_left = y_parab[x <= 0]
x_right = x[x >= 0]
y_right = y_parab[x >= 0]

# Zone au dessus de la parabole à gauche
# Polygone fermé : commence à x=0,x=0 → longe la parabole → descend à x=0,y=-max_parabole -> ferme
fig.add_trace(
    go.Scatter(
        x=np.concatenate(
            [[0], x_left[::-1], [0]]
        ),  # x=0 → parabole gauche vers 0 → x=0
        y=np.concatenate(
            [[0], y_left[::-1], [y_left[0]]]
        ),  # y=0 → parabole → revenir au bord
        mode="lines+markers",
        fill="toself",
        fillcolor="rgba(255,165,0,0.3)",  # orange pastel
        line=dict(color="rgba(0,0,0,0)"),
        name="upper left parabola",
        meta="ulp",
        hoverinfo="none",
        hoveron="points+fills",
        showlegend=False,
    )
)

# Zone au-dessus de la parabole à droite
# Polygone fermé : commence à x=0,y=0 → longe la parabole → descend à x=0,y=max_parabole → ferme
fig.add_trace(
    go.Scatter(
        x=np.concatenate([[0], x_right, [0]]),  # x=0 → parabole → x=0
        y=np.concatenate([[0], y_right, [y_right[-1]]]),  # y=0 → parabole → dernier y
        mode="lines+markers",
        fill="toself",
        fillcolor="rgba(0,191,255,0.3)",  # bleu ciel transparent
        line=dict(color="rgba(0,0,0,0)"),
        name="upper right parabola",
        meta="urp",
        hoverinfo="none",
        hoveron="points+fills",
        showlegend=False,
    )
)

# Zone sous la parabole à gauche
# Région gauche (x <= 0)
fig.add_trace(
    go.Scatter(
        x=np.concatenate([[-val_max], x_left, [0]]),  # de la gauche jusqu'à 0
        y=np.concatenate([[y_left[-1]], y_left, [0]]),  # bas à parabole
        mode="lines+markers",
        fill="toself",
        fillcolor="rgba(255,182,193,0.4)",  # rose pastel
        line=dict(color="rgba(0,0,0,0)"),
        name="lower left parabola",
        meta="llp",
        hoverinfo="none",
        hoveron="points+fills",
        showlegend=False,
    )
)

# Zone sous la parabole à droite
# Région droite (x >= 0)
fig.add_trace(
    go.Scatter(
        x=np.concatenate([[0], x_right, [val_max]]),  # de 0 à la droite
        y=np.concatenate([[y_right[0]], y_right, [0]]),  # parabole jusqu'au bas
        mode="lines+markers",
        fill="toself",
        fillcolor="rgba(100,149,237,0.2)",  # bleu pastel
        line=dict(color="rgba(0,0,0,0)"),
        name="lower right parabola",
        meta="lrp",
        hoverinfo="none",
        hoveron="points+fills",
        showlegend=False,
    )
)

# Zone sous l'axe x
fig.add_trace(
    go.Scatter(
        x=[-val_max, val_max, val_max, -val_max],
        y=[0, 0, -val_max, -val_max],
        mode="lines+markers",
        fill="toself",
        fillcolor="rgba(211,211,211,0.5)",  # gris pastel
        line=dict(color="rgba(0,0,0,0)"),
        name="lower x axis",
        meta="lxa",
        hoverinfo="none",
        hoveron="points+fills",
        showlegend=False,
    )
)

# Courbes principales
fig.add_trace(
    go.Scatter(
        x=[0, 0],
        y=[0, val_max],
        mode="lines",
        line=dict(color="rgba(100,149,237,0.9)", width=line_width),
        name="y line",
        meta="y",
        hoverinfo="none",
        showlegend=False,
    )
)
fig.add_trace(
    go.Scatter(
        x=[-val_max, val_max],
        y=[0, 0],
        mode="lines",
        line=dict(color="rgba(100,149,237,0.9)", width=line_width),
        name="x line",
        meta="x",
        hoverinfo="none",
        showlegend=False,
    )
)
fig.add_trace(
    go.Scatter(
        x=x,
        y=y_parab,
        mode="lines",
        line=dict(color="rgba(100,149,237,0.9)", width=line_width),
        name="parabola line",
        meta="parabola",
        hoverinfo="none",
        showlegend=False,
    )
)

# Layout
fig.update_layout(
    xaxis=dict(
        showgrid=False, zeroline=False, visible=False, range=[-val_max, val_max]
    ),
    yaxis=dict(
        showgrid=False, zeroline=False, visible=False, range=[-val_max, val_max]
    ),
    plot_bgcolor="white",
    margin=dict(l=0, r=0, t=0, b=0),
)

app.layout = html.Div(
    [
        dcc.Graph(id="graph", figure=fig, config={"displayModeBar": False}),
        html.Div(id="output"),
    ]
)


@app.callback(Output("output", "children"), Input("graph", "clickData"))
def display_click_data(clickData):
    if clickData:
        point = clickData["points"][0]
        trace_id = point.get("curveNumber")
        meta = point.get("data", {}).get("meta")
        return f"Trace cliquée : {trace_id}, id = {meta}"
    return "Clique sur une trace"


if __name__ == "__main__":
    app.run(debug=True)
