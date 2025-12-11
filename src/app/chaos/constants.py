"""
Constantes pour la simulation du problème à trois corps.
"""

from src.app.style.palette import PALETTE

# Physique de la simulation
GRAVITATIONAL_CONSTANT = 1.0
SOFTENING_PARAMETER = 0.15  # Paramètre d'adoucissement pour éviter les singularités
MAX_ACCELERATION = 10.0  # Limite d'accélération pour la stabilité numérique

# Configuration par défaut des corps
DEFAULT_MASSES = [1.0, 0.8, 1.2]  # Masses asymétriques pour induire le chaos
DEFAULT_RADII = [0.1, 0.1, 0.1]
DEFAULT_COLORS = [
    PALETTE.primary,  # Corps 1: Orange primaire #EA580C
    PALETTE.secondary,  # Corps 2: Rouge secondaire #DC2626
    PALETTE.stability_stable,  # Corps 3: Vert stabilité #27ae60
]
DEFAULT_BODY_NAMES = ["Corps 1", "Corps 2", "Corps 3"]

# Positions initiales de base (triangle avec coordonnées à chiffres ronds)
DEFAULT_POSITIONS = [
    [0.0, 2.0],  # Corps 1: sommet supérieur
    [-2.0, -1.0],  # Corps 2: sommet inférieur gauche
    [2.0, -1.0],  # Corps 3: sommet inférieur droit
]

# Paramètres de configuration initiale
DEFAULT_SPEED_SCALE = 0.2
DEFAULT_RANDOMIZATION_FACTOR = 0.05  # Amplitude des perturbations aléatoires

# Facteurs de vitesse initiale par corps
SPEED_FACTORS = [0.3, 0.5, 0.4]
RADIAL_COMPONENT_RATIO = 0.25  # Proportion de composante radiale dans la vitesse

# Paramètres de simulation
DEFAULT_TOTAL_TIME = 20.0  # secondes
DEFAULT_TIME_STEP = 0.02  # secondes

# Paramètres de visualisation
PLOT_TOTAL_TIME = 30.0  # Durée de simulation: 30 secondes
PLOT_AXIS_RANGE = [-3, 3]
MAX_ANIMATION_FRAMES = 300  # Nombre maximal de frames à afficher

# Styles d'animation
TRAJECTORY_LINE_WIDTH = 1.5
TRAJECTORY_OPACITY = 0.5
BODY_MARKER_SIZE = 18
ANIMATION_FRAME_DURATION = 100  # millisecondes

# Couleurs du thème
PLOT_BACKGROUND_COLOR = "#0b1021"
TIME_ANNOTATION_BACKGROUND = "rgba(11, 16, 33, 0.7)"
TIME_ANNOTATION_BORDER = "#ffffff"
TIME_ANNOTATION_FONT_COLOR = "#ffffff"
TIME_ANNOTATION_FONT_SIZE = 14
