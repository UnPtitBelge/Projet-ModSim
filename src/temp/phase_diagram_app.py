from dash import Dash, dcc, html, Input, Output
from phase_diagram import create_phase_diagram, EQUILIBRIUM_SYSTEMS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Diagramme de Phase Interactif", 
            style={"textAlign": "center", "marginTop": "20px", "marginBottom": "30px"}),
    
    html.Div([
        # Sélecteur de type d'équilibre
        html.Div([
            html.Label("Type de point d'équilibre:", style={"fontWeight": "bold", "marginRight": "10px"}),
            dcc.Dropdown(
                id='dropdown-equilibrium-type',
                options=[
                    {'label': eq_type.replace('_', ' ').title(), 'value': eq_type}
                    for eq_type in sorted(EQUILIBRIUM_SYSTEMS.keys())
                ],
                value='foyer_stable',
                style={"width": "100%"}
            ),
        ], style={
            "width": "90%",
            "margin": "0 auto 20px",
            "padding": "15px",
            "border": "1px solid #ddd",
            "borderRadius": "5px",
            "backgroundColor": "#f9f9f9"
        }),
        
        # Mode personnalisé
        html.Div([
            dcc.Checklist(
                id='checklist-custom-params',
                options=[{'label': ' Mode personnalisé', 'value': 'custom'}],
                value=[],
                style={"marginBottom": "15px"}
            ),
            
            html.Div(id='custom-params-section', style={"display": "none"}, children=[
                html.Div([
                    html.Label('Paramètre a (dx/dt = ax + by):', style={"fontWeight": "bold", "display": "block", "marginBottom": "5px"}),
                    dcc.Slider(
                        id='slider-a',
                        min=-3, max=3, step=0.1,
                        value=-1,
                        marks={i: str(i) for i in range(-3, 4)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], style={"marginBottom": "20px"}),
                
                html.Div([
                    html.Label('Paramètre b (dx/dt = ax + by):', style={"fontWeight": "bold", "display": "block", "marginBottom": "5px"}),
                    dcc.Slider(
                        id='slider-b',
                        min=-3, max=3, step=0.1,
                        value=1,
                        marks={i: str(i) for i in range(-3, 4)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], style={"marginBottom": "20px"}),
                
                html.Div([
                    html.Label('Paramètre c (dy/dt = cx + dy):', style={"fontWeight": "bold", "display": "block", "marginBottom": "5px"}),
                    dcc.Slider(
                        id='slider-c',
                        min=-3, max=3, step=0.1,
                        value=-1,
                        marks={i: str(i) for i in range(-3, 4)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], style={"marginBottom": "20px"}),
                
                html.Div([
                    html.Label('Paramètre d (dy/dt = cx + dy):', style={"fontWeight": "bold", "display": "block", "marginBottom": "5px"}),
                    dcc.Slider(
                        id='slider-d',
                        min=-3, max=3, step=0.1,
                        value=-1,
                        marks={i: str(i) for i in range(-3, 4)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                ], style={"marginBottom": "0px"}),
            ])
            
        ], style={
            "width": "90%",
            "margin": "0 auto 20px",
            "padding": "15px",
            "border": "1px solid #ddd",
            "borderRadius": "5px",
            "backgroundColor": "#f9f9f9"
        }),
    ]),
    
    # Graphique
    html.Div([
        dcc.Graph(id='phase-diagram')
    ], style={"width": "95%", "margin": "20px auto"}),
    
    html.Footer(
        "Diagramme de phase - Trajectoires espacées de 0.5",
        style={"textAlign": "center", "marginTop": "30px", "color": "gray", "fontSize": "12px", "paddingBottom": "20px"}
    )
])

# Callback 1: Basculer l'affichage de la section personnalisée
@app.callback(
    Output('custom-params-section', 'style'),
    Input('checklist-custom-params', 'value')
)
def toggle_custom_params(custom_params):
    return {"display": "block"} if 'custom' in custom_params else {"display": "none"}

# Callback 2: Mise à jour du diagramme
@app.callback(
    Output('phase-diagram', 'figure'),
    [
        Input('dropdown-equilibrium-type', 'value'),
        Input('checklist-custom-params', 'value'),
        Input('slider-a', 'value'),
        Input('slider-b', 'value'),
        Input('slider-c', 'value'),
        Input('slider-d', 'value'),
    ]
)
def update_phase_diagram(equilibrium_type, custom_params, a, b, c, d):
    """Mise à jour du diagramme de phase"""
    use_custom = 'custom' in custom_params
    
    # Si mode personnalisé n'est pas activé, utiliser None (mode prédéfini)
    if not use_custom:
        a = b = c = d = None
    
    logger.info(f"Update: type={equilibrium_type}, custom={use_custom}, a={a}, b={b}, c={c}, d={d}")
    
    fig = create_phase_diagram(
        equilibrium_type=equilibrium_type,
        a=a, b=b, c=c, d=d,
        custom_params=use_custom
    )
    return fig

if __name__ == '__main__':
    logger.info("Démarrage sur http://localhost:8050")
    app.run(debug=True, port=8050)