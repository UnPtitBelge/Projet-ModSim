import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go
import logging

logger = logging.getLogger(__name__)

# Définition des systèmes pour chaque type d'équilibre
EQUILIBRIUM_SYSTEMS = {
    'centre': {
        'a': 0, 'b': 1, 'c': -1, 'd': 0,
        'description': 'Centre: trajectoires fermées (orbites périodiques)'
    },
    'foyer_stable': {
        'a': -1, 'b': 1, 'c': -1, 'd': -1,
        'description': 'Foyer stable: spirales convergeant vers l\'équilibre'
    },
    'foyer_instable': {
        'a': 1, 'b': 1, 'c': -1, 'd': 1,
        'description': 'Foyer instable: spirales divergeant de l\'équilibre'
    },
    'noeud_stable': {
        'a': -2, 'b': 0, 'c': 0, 'd': -1,
        'description': 'Nœud stable: convergence directe vers l\'équilibre'
    },
    'noeud_instable': {
        'a': 2, 'b': 0, 'c': 0, 'd': 1,
        'description': 'Nœud instable: divergence directe de l\'équilibre'
    },
    'noeud_stable_degenere': {
        'a': -1, 'b': 1, 'c': 0, 'd': -1,
        'description': 'Nœud stable dégénéré: convergence lente'
    },
    'noeud_instable_degenere': {
        'a': 1, 'b': 1, 'c': 0, 'd': 1,
        'description': 'Nœud instable dégénéré: divergence lente'
    },
    'selle': {
        'a': 1, 'b': 0, 'c': 0, 'd': -1,
        'description': 'Selle: directions stables et instables'
    },
    'ligne_pe_stable': {
        'a': -1, 'b': 0, 'c': 0, 'd': 0,
        'description': 'Ligne propre stable: convergence vers une droite'
    },
    'ligne_pe_instable': {
        'a': 1, 'b': 0, 'c': 0, 'd': 0,
        'description': 'Ligne propre instable: divergence depuis une droite'
    },
    'mouvement_uniforme': {
        'a': 0, 'b': 1, 'c': 0, 'd': 0,
        'description': 'Mouvement uniforme: trajectoires parallèles'
    }
}

def create_phase_diagram(equilibrium_type='foyer_stable', a=None, b=None, c=None, d=None, 
                         custom_params=False):
    """
    Crée un diagramme de phase pour un système 2D optimisé
    
    Système: dx/dt = a*x + b*y
             dy/dt = c*x + d*y
    
    Args:
        equilibrium_type: Type de point d'équilibre
        a, b, c, d: Paramètres de la matrice Jacobienne
        custom_params: Si True, utilise les paramètres fournis
    
    Returns:
        Figure Plotly
    """
    
    # Récupérer les paramètres
    if custom_params and all(param is not None for param in [a, b, c, d]):
        logger.info(f"Paramètres personnalisés: a={a}, b={b}, c={c}, d={d}")
    else:
        if equilibrium_type not in EQUILIBRIUM_SYSTEMS:
            equilibrium_type = 'foyer_stable'
        
        params = EQUILIBRIUM_SYSTEMS[equilibrium_type]
        a, b, c, d = params['a'], params['b'], params['c'], params['d']
        logger.info(f"Type: {equilibrium_type}")
    
    fig = go.Figure()
    
    # Définir le système
    def system(state, t):
        x_var, y_var = state
        return [a*x_var + b*y_var, c*x_var + d*y_var]
    
    # Générer les conditions initiales espacées de 1.5 (réduction pour vitesse)
    initial_conditions = []
    for x0 in np.arange(-3, 3.5, 1.5):
        for y0 in np.arange(-3, 3.5, 1.5):
            initial_conditions.append((x0, y0))
    
    logger.info(f"Nombre de trajectoires: {len(initial_conditions)}")
    
    # Détecter le type de système
    trace = a + d
    det = a * d - b * c
    
    # Cas particuliers
    is_centre = (trace == 0 and det > 0)  # Centre: trajectoires fermées
    is_mouvement_uniforme = (trace == 0 and det == 0)  # Mouvement uniforme
    is_selle = (det < 0)  # Selle: déterminant négatif
    is_unstable = trace > 0 or (det < 0 and trace > 0)
    
    # Adapter le temps d'intégration selon le type
    if is_mouvement_uniforme:
        t = np.linspace(0, 4, 40)  # Temps moyen pour voir les trajectoires parallèles
        logger.info("Mouvement uniforme - intégration adaptée")
    elif is_selle:
        t = np.linspace(0, 2, 35)  # Temps court pour rester lisible
        logger.info("Selle - intégration adaptée")
    elif is_centre:
        t = np.linspace(0, 2*np.pi, 50)  # Une période complète
        logger.info("Centre - intégration adaptée")
    elif is_unstable:
        t = np.linspace(0, 1.5, 30)  # Temps très court pour rester dans la zone
        logger.info("Système instable - intégration réduite")
    else:
        t = np.linspace(0, 8, 50)  # Temps normal pour les systèmes stables
    
    # Suivre les limites des trajectoires
    x_min, x_max = 0, 0
    y_min, y_max = 0, 0
    
    # Stocker les trajectoires pour tracer les flèches
    trajectories = []
    
    # Générer les trajectoires (pour les limites et les flèches)
    total_trajectories = len(initial_conditions)
    logger.info("Début de la génération des trajectoires...")
    
    for idx_traj, (x0, y0) in enumerate(initial_conditions):
        try:
            # Log de progression tous les 10 trajectoires
            if idx_traj % 10 == 0:
                logger.info(f"  Trajectoire {idx_traj + 1}/{total_trajectories} ({100 * idx_traj / total_trajectories:.1f}%)")
            
            traj = odeint(system, [x0, y0], t, full_output=False)
            trajectories.append(traj)
            
            # Mettre à jour les limites
            x_min = min(x_min, np.min(traj[:, 0]))
            x_max = max(x_max, np.max(traj[:, 0]))
            y_min = min(y_min, np.min(traj[:, 1]))
            y_max = max(y_max, np.max(traj[:, 1]))
        except Exception as e:
            logger.warning(f"  Erreur pour trajectoire ({x0}, {y0}): {e}")
    
    logger.info(f"Trajectoires générées: {total_trajectories}/{total_trajectories} (100%)")
    
    # Ajouter le point d'équilibre
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        marker=dict(size=10, color='red', symbol='diamond'),
        name='Équilibre',
        hoverinfo='text',
        hovertext='(0, 0)',
        showlegend=True
    ))
    
    # Calculer les marges (10% de la plage)
    margin_x = (x_max - x_min) * 0.1 if x_max != x_min else 0.5
    margin_y = (y_max - y_min) * 0.1 if y_max != y_min else 0.5
    
    # Définir les limites avec marges
    x_range = [x_min - margin_x, x_max + margin_x]
    y_range = [y_min - margin_y, y_max + margin_y]
    
    # Adapter les limites selon le type de système
    standard_range = 3.6
    
    if is_mouvement_uniforme:
        # Mouvement uniforme: trajectoires parallèles - plage plus large en x
        x_range = [-5, 5]
        y_range = [-standard_range, standard_range]
        logger.info("Mouvement uniforme - plage adaptée")
    elif is_selle:
        # Selle: même plage que les stables
        x_range = [-standard_range, standard_range]
        y_range = [-standard_range, standard_range]
        logger.info("Selle - échelle standard")
    elif is_centre:
        # Centre: trajectoires fermées - même plage
        x_range = [-standard_range, standard_range]
        y_range = [-standard_range, standard_range]
        logger.info("Centre - échelle standard")
    elif is_unstable:
        # Systèmes instables: même plage que les stables
        x_range = [-standard_range, standard_range]
        y_range = [-standard_range, standard_range]
        logger.info(f"Système instable - échelle fixe: ±{standard_range}")
    
    logger.info(f"Limites x: {x_range}, Limites y: {y_range}")
    
    # MAINTENANT ajouter une grille de flèches équitablement espacées sur le graphe
    logger.info("Ajout des flèches espacées sur le graphe...")
    total_arrows = 0
    
    # Créer une grille de points régulièrement espacés
    grid_density = 15  # Nombre de flèches par axe (15x15 = 225 flèches)
    x_arrow_positions = np.linspace(x_range[0], x_range[1], grid_density)
    y_arrow_positions = np.linspace(y_range[0], y_range[1], grid_density)
    
    logger.info(f"Grille de flèches: {grid_density}x{grid_density} = {grid_density**2} flèches")
    
    # Vectoriser le calcul des normes pour vitesse (au lieu de boucles)
    X, Y = np.meshgrid(x_arrow_positions, y_arrow_positions)
    velocities_x = a * X + b * Y
    velocities_y = c * X + d * Y
    norms = np.sqrt(velocities_x**2 + velocities_y**2).flatten()
    
    # Filtrer les normes valides
    valid_norms = norms[norms > 0.01]
    
    if len(valid_norms) > 0:
        norm_min = np.min(valid_norms)
        norm_max = np.max(valid_norms)
        norm_range = norm_max - norm_min if norm_max != norm_min else 1
    else:
        norm_min, norm_max, norm_range = 0, 1, 1
    
    logger.info(f"Intensités: min={norm_min:.3f}, max={norm_max:.3f}")
    
    # Collecter toutes les flèches et les ajouter efficacement
    arrow_data_x = []
    arrow_data_y = []
    arrow_tail_x = []
    arrow_tail_y = []
    arrow_angles = []  # Stocker les angles pour orienter les marqueurs
    
    # Utiliser une échelle logarithmique pour gérer les grandes variations d'intensité
    norm_min_log = np.log(norm_min + 1)
    norm_max_log = np.log(norm_max + 1)
    norm_range_log = norm_max_log - norm_min_log if norm_max_log != norm_min_log else 1
    
    for x_pos in x_arrow_positions:
        for y_pos in y_arrow_positions:
            # Calculer la norme (intensité)
            dx = a * x_pos + b * y_pos
            dy = c * x_pos + d * y_pos
            norm = np.sqrt(dx**2 + dy**2)
            
            if norm > 0.01:  # Éviter les flèches trop petites
                dx_norm = dx / norm
                dy_norm = dy / norm
                
                # Normaliser l'intensité en échelle logarithmique pour les grandes variations
                norm_log = np.log(norm + 1)
                intensity_normalized = (norm_log - norm_min_log) / norm_range_log if norm_range_log > 0 else 0.5
                intensity_normalized = np.clip(intensity_normalized, 0, 1)  # Borner entre 0 et 1
                
                # Appliquer une fonction puissance pour amplifier les faibles intensités
                # Utiliser 0.5 au lieu de 0.7 pour amplifier davantage les faibles valeurs
                intensity_amplified = intensity_normalized ** 0.5
                
                # Offset augmenté: entre 0.2 et 0.6 pour des flèches plus visibles
                offset = 0.2 + intensity_amplified * 0.4
                
                x_tail = x_pos - dx_norm * offset
                y_tail = y_pos - dy_norm * offset
                
                # Calculer l'angle en radians pour orienter la flèche
                angle = np.arctan2(dy_norm, dx_norm)
                
                # Ajouter au vecteur de flèches
                arrow_data_x.append(x_pos)
                arrow_data_y.append(y_pos)
                arrow_tail_x.append(x_tail)
                arrow_tail_y.append(y_tail)
                arrow_angles.append(angle)
                total_arrows += 1
    
    # Ajouter les segments et les têtes de flèche en Scatter (rapide)
    if arrow_data_x:
        # Créer tous les segments de flèches à la fois
        for i in range(len(arrow_data_x)):
            fig.add_trace(go.Scatter(
                x=[arrow_tail_x[i], arrow_data_x[i]],
                y=[arrow_tail_y[i], arrow_data_y[i]],
                mode='lines',
                line=dict(color='#1f77b4', width=1),
                hoverinfo='skip',
                showlegend=False
            ))
        
        # Ajouter les têtes de flèche orientées avec des petites lignes en V
        # Créer les points des deux côtés du triangle pour chaque flèche
        head_angle = np.pi / 6  # 30 degrés pour les pointes latérales
        head_length = 0.15
        
        for i in range(len(arrow_data_x)):
            angle = arrow_angles[i]
            
            # Points des deux pointes du triangle
            angle_left = angle + head_angle
            angle_right = angle - head_angle
            
            p1_x = arrow_data_x[i] - head_length * np.cos(angle_left)
            p1_y = arrow_data_y[i] - head_length * np.sin(angle_left)
            
            p2_x = arrow_data_x[i] - head_length * np.cos(angle_right)
            p2_y = arrow_data_y[i] - head_length * np.sin(angle_right)
            
            # Ajouter les deux lignes du triangle
            fig.add_trace(go.Scatter(
                x=[arrow_data_x[i], p1_x],
                y=[arrow_data_y[i], p1_y],
                mode='lines',
                line=dict(color='#1f77b4', width=1.5),
                hoverinfo='skip',
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=[arrow_data_x[i], p2_x],
                y=[arrow_data_y[i], p2_y],
                mode='lines',
                line=dict(color='#1f77b4', width=1.5),
                hoverinfo='skip',
                showlegend=False
            ))
    
    logger.info(f"Flèches ajoutées: {total_arrows}")
    
    # Déterminer le titre
    title = f"Diagramme de phase - {equilibrium_type.replace('_', ' ').title()}"
    if equilibrium_type in EQUILIBRIUM_SYSTEMS:
        subtitle = EQUILIBRIUM_SYSTEMS[equilibrium_type]['description']
        title = f"{title}<br><sub>{subtitle}</sub>"
    
    fig.update_layout(
        title=title,
        xaxis_title='x',
        yaxis_title='y',
        hovermode='closest',
        width=900,
        height=750,
        xaxis=dict(
            range=x_range, 
            scaleanchor='y', 
            scaleratio=1
        ),
        yaxis=dict(
            range=y_range, 
            scaleanchor='x', 
            scaleratio=1
        ),
        font=dict(size=11),
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
        paper_bgcolor='white',
        # Boutons de contrôle du zoom
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=[
                    dict(
                        args=[{"xaxis.range": x_range, "yaxis.range": y_range}],
                        label="Réinitialiser vue",
                        method="relayout"
                    )
                ],
                pad={"r": 10, "t": 10},
                showactive=False,
                x=0.0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            ),
        ]
    )
    
    # Vérification finale
    final_annotations = len(fig.layout.annotations) if fig.layout.annotations else 0
    logger.info(f"Diagramme créé avec succès - {final_annotations} annotations dans la figure finale")
    return fig