"""Profiling pour identifier les parties lentes de create_phase_diagram"""

import time
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go
from phase_diagram import EQUILIBRIUM_SYSTEMS

def profile_phase_diagram():
    """Profile chaque étape de la création du diagramme"""
    
    equilibrium_type = 'foyer_stable'
    params = EQUILIBRIUM_SYSTEMS[equilibrium_type]
    a, b, c, d = params['a'], params['b'], params['c'], params['d']
    
    print("\n" + "="*70)
    print("PROFILING DE LA CRÉATION DU DIAGRAMME DE PHASE")
    print("="*70)
    
    # Étape 1: Génération des conditions initiales
    t0 = time.time()
    initial_conditions = []
    for x0 in np.arange(-3, 3.5, 1.0):
        for y0 in np.arange(-3, 3.5, 1.0):
            initial_conditions.append((x0, y0))
    t1 = time.time()
    print(f"\n[1] Génération conditions initiales ({len(initial_conditions)} points)")
    print(f"    Temps: {(t1-t0)*1000:.2f} ms")
    
    # Étape 2: Calcul des trajectoires (sans plotting)
    def system(state, t):
        x_var, y_var = state
        return [a*x_var + b*y_var, c*x_var + d*y_var]
    
    t = np.linspace(0, 8, 100)
    
    t0 = time.time()
    all_trajectories = []
    for x0, y0 in initial_conditions:
        try:
            traj = odeint(system, [x0, y0], t, full_output=False)
            all_trajectories.append(traj)
        except:
            pass
    t1 = time.time()
    print(f"\n[2] Calcul des {len(all_trajectories)} trajectoires (odeint)")
    print(f"    Temps: {(t1-t0)*1000:.2f} ms")
    print(f"    Temps par trajectoire: {(t1-t0)*1000/len(all_trajectories):.2f} ms")
    
    # Étape 3: Création des traces Scatter
    fig = go.Figure()
    t0 = time.time()
    for traj in all_trajectories:
        fig.add_trace(go.Scatter(
            x=traj[:, 0], y=traj[:, 1],
            mode='lines',
            line=dict(color='#1f77b4', width=1.5),
            name='',
            hoverinfo='skip',
            showlegend=False
        ))
    t1 = time.time()
    print(f"\n[3] Ajout de {len(all_trajectories)} traces Scatter")
    print(f"    Temps: {(t1-t0)*1000:.2f} ms")
    print(f"    Temps par trace: {(t1-t0)*1000/len(all_trajectories):.2f} ms")
    
    # Étape 4: Ajout des flèches (annotations)
    t0 = time.time()
    arrow_count = 0
    arrow_spacing = 8
    for traj in all_trajectories:
        for idx in range(arrow_spacing, len(traj) - 1, arrow_spacing):
            dx = traj[idx + 1, 0] - traj[idx - 1, 0]
            dy = traj[idx + 1, 1] - traj[idx - 1, 1]
            norm = np.sqrt(dx**2 + dy**2)
            if norm > 0.01:
                fig.add_annotation(
                    x=traj[idx, 0],
                    y=traj[idx, 1],
                    ax=traj[idx, 0] - dx * 0.15,
                    ay=traj[idx, 1] - dy * 0.15,
                    xref='x', yref='y',
                    axref='x', ayref='y',
                    showarrow=True,
                    arrowhead=3,
                    arrowsize=1.5,
                    arrowwidth=2.5,
                    arrowcolor='#1f77b4'
                )
                arrow_count += 1
    t1 = time.time()
    print(f"\n[4] Ajout de {arrow_count} flèches (annotations)")
    print(f"    Temps: {(t1-t0)*1000:.2f} ms")
    print(f"    Temps par flèche: {(t1-t0)*1000/arrow_count:.2f} ms")
    
    # Étape 5: Configuration du layout
    t0 = time.time()
    fig.update_layout(
        title="Test",
        xaxis_title='x',
        yaxis_title='y',
        width=900,
        height=750
    )
    t1 = time.time()
    print(f"\n[5] Configuration du layout")
    print(f"    Temps: {(t1-t0)*1000:.2f} ms")
    
    print("\n" + "="*70)
    print("RÉSUMÉ")
    print("="*70)
    print(f"Total trajectoires: {len(all_trajectories)}")
    print(f"Total flèches: {arrow_count}")
    print(f"Total traces Plotly: {len(fig.data)}")
    print(f"Total annotations: {len(fig.layout.annotations) if fig.layout.annotations else 0}")
    
    print("\n⚠️  GOULOTS D'ÉTRANGLEMENT POTENTIELS:")
    print("   - Si 'Ajout des flèches' > 1000ms → trop d'annotations")
    print("   - Si 'Calcul des trajectoires' > 500ms → odeint trop lent")
    print("   - Si 'Ajout traces Scatter' > 500ms → trop de traces")
    print("="*70 + "\n")

if __name__ == '__main__':
    profile_phase_diagram()
