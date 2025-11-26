"""
Constantes globales pour le diagramme de Poincaré:
- bornes τ (TAU_MIN, TAU_MAX)
- résolution d'échantillonnage (N_SAMPLES)
- delta max (DELTA_MAX)
- couleurs (BASE_COLOR, HOVER_COLOR, CLICK_COLOR)
- labels des zones (ZONE_LABELS / get_zone_label)
"""

# Numeric bounds for τ (tau)
TAU_MIN: float = -10.0
TAU_MAX: float = 10.0

# Sampling resolution for tau axis (and derived curves)
N_SAMPLES: int = 300

# Derived constant: maximum delta reached by the parabola at TAU_MAX
# Parabola in current model: delta = tau^2 / 4
DELTA_MAX: float = (TAU_MAX**2) / 4.0

# Base colors (semi‑transparent RGBA for better axis readability)
BASE_COLOR: str = "rgba(210, 70, 70, 0.35)"
HOVER_COLOR: str = "rgba(240, 150, 150, 0.55)"
CLICK_COLOR: str = "rgba(150, 30, 30, 0.65)"

# Mapping from curveNumber (Plotly trace index) to human‑readable labels
# 0 is the parabola line; 1..5 are the filled stability zones.
ZONE_LABELS = {
    0: "Parabole",
    1: "Zone supérieure gauche",
    2: "Zone supérieure droite",
    3: "Zone inférieure gauche",
    4: "Zone inférieure droite",
    5: "Zone inférieure",
}


def get_zone_label(curve_number: int) -> str:
    """
    Return a user-facing label for a given Plotly trace index (curveNumber).
    Falls back to 'Zone inconnue' if the index is not recognized.
    """
    return ZONE_LABELS.get(curve_number, "Zone inconnue")


__all__ = [
    "TAU_MIN",
    "TAU_MAX",
    "N_SAMPLES",
    "DELTA_MAX",
    "BASE_COLOR",
    "HOVER_COLOR",
    "CLICK_COLOR",
    "ZONE_LABELS",
    "get_zone_label",
]
