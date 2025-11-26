from dash import Dash, dcc, html, Input, Output
import numpy as np
import plotly.graph_objs as go

# Initialisation de l'application Dash
app = Dash(__name__)

# Données pour la parabole et les surfaces
x = np.linspace(-10, 10, 200)
y_parabole = (x**2) / 4

# Mise en page de l'application
app.layout = html.Div([
    dcc.Graph(
        id='graph',
        figure={
            'data': [
                # Surface en haut à gauche
                go.Scatter(
                    x=np.concatenate([x[x < 0], x[x < 0][::-1]]),
                    y=np.concatenate([y_parabole[x < 0], [max(y_parabole) + 10] * len(x[x < 0])]),
                    fill='toself',
                    fillcolor='rgba(255, 0, 0, 0.2)',
                    line=dict(width=0),
                    name='Haut gauche',
                    hoverinfo='none'
                ),
                # Surface en haut à droite
                go.Scatter(
                    x=np.concatenate([x[x > 0], x[x > 0][::-1]]),
                    y=np.concatenate([y_parabole[x > 0], [max(y_parabole) + 10] * len(x[x > 0])]),
                    fill='toself',
                    fillcolor='rgba(0, 255, 0, 0.2)',
                    line=dict(width=0),
                    name='Haut droite',
                    hoverinfo='none'
                ),
                # Surface en bas à gauche
                go.Scatter(
                    x=np.concatenate([x[x < 0], x[x < 0][::-1]]),
                    y=np.concatenate([y_parabole[x < 0], [min(y_parabole) - 10] * len(x[x < 0])]),
                    fill='toself',
                    fillcolor='rgba(0, 0, 255, 0.2)',
                    line=dict(width=0),
                    name='Bas gauche',
                    hoverinfo='none'
                ),
                # Surface en bas à droite
                go.Scatter(
                    x=np.concatenate([x[x > 0], x[x > 0][::-1]]),
                    y=np.concatenate([y_parabole[x > 0], [min(y_parabole) - 10] * len(x[x > 0])]),
                    fill='toself',
                    fillcolor='rgba(255, 255, 0, 0.2)',
                    line=dict(width=0),
                    name='Bas droite',
                    hoverinfo='none'
                ),
                # Tracé de la parabole
                go.Scatter(
                    x=x, y=y_parabole, mode='lines', line=dict(color='blue'),
                    name='Parabole'
                )
            ],
            'layout': go.Layout(
                title='Surfaces autour d\'une parabole',
                xaxis=dict(title='x'),
                yaxis=dict(title='y'),
                hovermode='closest'
            )
        }
    ),
    html.Div(id='output', style={'marginTop': '20px'})
])

# Callback pour capturer les clics et identifier la surface
@app.callback(
    Output('output', 'children'),
    Input('graph', 'clickData')  # On écoute les clics sur le graphe
)
def identify_surface(clickData):
    if clickData is None or 'points' not in clickData or not clickData['points']:
        return "Cliquez sur une zone du graphe pour l'identifier."

    # Debug: Afficher les données de clic pour inspection
    print(clickData)

    # Extraction des informations de clic
    point = clickData['points'][0]

    # Vérification si les coordonnées x et y sont disponibles
    if 'bbox' in point:
        bbox = point['bbox']
        x_clicked = (bbox['x0'] + bbox['x1']) / 2  # Calculer la position x moyenne
        y_clicked = (bbox['y0'] + bbox['y1']) / 2  # Calculer la position y moyenne
    else:
        return "Données de clic invalides. Veuillez réessayer."

    # Vérifier si le numéro de courbe (curveNumber) est présent
    curve_number = point.get('curveNumber', None)
    x_clicked = point.get('x', None)  # Récupérer la position x pour la parabole

    if curve_number is None:
        return "Données de clic invalides. Veuillez réessayer."

    # Associer le clic à la zone ou à la parabole en fonction de curveNumber
    if curve_number == 0:
        return "Vous avez cliqué dans la zone HAUT GAUCHE."
    elif curve_number == 1:
        return "Vous avez cliqué dans la zone HAUT DROITE."
    elif curve_number == 2:
        return "Vous avez cliqué dans la zone BAS GAUCHE."
    elif curve_number == 3:
        return "Vous avez cliqué dans la zone BAS DROITE."
    elif curve_number == 4:
        if x_clicked is not None:
            if x_clicked < 0:
                return "Vous avez cliqué sur la partie gauche (x négatif) de la parabole."
            else:
                return "Vous avez cliqué sur la partie droite (x positif) de la parabole."
        else:
            return "Vous avez cliqué sur la parabole, mais la position x est inconnue."
    else:
        return "Le clic ne correspond à aucune zone définie."

# Lancement de l'application
if __name__ == '__main__':
    app.run(debug=True)