"""
Constantes numériques pour le diagramme de Poincaré:
- bornes τ (TAU_MIN, TAU_MAX)
- résolution d'échantillonnage (N_SAMPLES)
- delta max (DELTA_MAX)
"""

# Bornes pour τ
TAU_MIN: float = -10.0
TAU_MAX: float = 10.0

# Résolution d'échantillonnage
N_SAMPLES: int = 300

# Delta maximal (parabole τ^2 / 4 évaluée en TAU_MAX)
DELTA_MAX: float = (TAU_MAX**2) / 4.0

__all__ = ["TAU_MIN", "TAU_MAX", "N_SAMPLES", "DELTA_MAX"]
