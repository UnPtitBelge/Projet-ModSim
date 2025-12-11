"""
Simulation du problème à trois corps.

Implémente la simulation numérique de trois corps soumis à l'attraction gravitationnelle,
avec une configuration initiale en triangle équilatéral pour favoriser le comportement chaotique.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from src.app.chaos.constants import (DEFAULT_BODY_NAMES, DEFAULT_COLORS,
                                     DEFAULT_MASSES, DEFAULT_POSITIONS,
                                     DEFAULT_RADII,
                                     DEFAULT_RANDOMIZATION_FACTOR,
                                     DEFAULT_SPEED_SCALE, DEFAULT_TIME_STEP,
                                     DEFAULT_TOTAL_TIME,
                                     GRAVITATIONAL_CONSTANT, MAX_ACCELERATION,
                                     RADIAL_COMPONENT_RATIO,
                                     SOFTENING_PARAMETER, SPEED_FACTORS)


@dataclass
class Body:
    """
    Représente un corps céleste dans la simulation du problème à trois corps.

    Attributes:
        mass: Masse du corps (unités normalisées)
        radius: Rayon du corps (pour la visualisation)
        position: Vecteur position 2D [x, y]
        velocity: Vecteur vitesse 2D [vx, vy]
        color: Couleur hexadécimale pour la visualisation
        name: Nom du corps pour l'identification
    """

    mass: float
    radius: float
    position: np.ndarray
    velocity: np.ndarray
    color: str
    name: str


def create_triangle_bodies(
    masses: List[float] = None,
    radii: List[float] = None,
    speed_scale: float = DEFAULT_SPEED_SCALE,
    randomize: bool = False,
    randomization_factor: float = DEFAULT_RANDOMIZATION_FACTOR,
) -> List[Body]:
    """
    Crée trois corps positionnés en triangle avec des coordonnées à chiffres ronds.

    Les positions sont choisies pour être faciles à visualiser:
    - Corps 1: (0, 2)     - en haut
    - Corps 2: (-2, -1)   - en bas à gauche
    - Corps 3: (2, -1)    - en bas à droite

    Args:
        masses: Masses des trois corps (défaut: masses asymétriques pour chaos)
        radii: Rayons des trois corps (pour visualisation)
        speed_scale: Facteur d'échelle pour les vitesses initiales
        randomize: Active l'ajout d'un bruit aléatoire aux positions
        randomization_factor: Amplitude du bruit aléatoire

    Returns:
        Liste de 3 objets Body avec positions et vitesses initiales
    """
    if masses is None:
        masses = DEFAULT_MASSES
    if radii is None:
        radii = DEFAULT_RADII

    # Positions à chiffres ronds pour une meilleure visualisation
    positions = np.array(DEFAULT_POSITIONS)

    # Ajouter une perturbation aléatoire pour varier les trajectoires
    if randomize:
        noise = np.random.normal(0, randomization_factor, positions.shape)
        positions = positions + noise

    # Calculer les vitesses initiales (tangentielles + composante radiale)
    velocities = []
    for idx, pos in enumerate(positions):
        # Direction tangentielle (perpendiculaire à la position)
        perp = np.array([-pos[1], pos[0]])
        norm_perp = np.linalg.norm(perp)
        tangential_dir = perp / norm_perp if norm_perp > 0 else np.zeros(2)

        # Direction radiale (vers l'extérieur)
        norm_pos = np.linalg.norm(pos)
        radial_dir = pos / norm_pos if norm_pos > 0 else np.zeros(2)

        # Combiner tangentielle et radiale
        velocity_dir = tangential_dir + RADIAL_COMPONENT_RATIO * radial_dir
        velocity_dir = velocity_dir / np.linalg.norm(velocity_dir)

        # Appliquer l'échelle et le facteur spécifique au corps
        velocities.append(velocity_dir * speed_scale * SPEED_FACTORS[idx])

    velocities = np.array(velocities)

    # Créer les objets Body
    return [
        Body(
            mass=masses[i],
            radius=radii[i],
            position=positions[i].copy(),
            velocity=velocities[i].copy(),
            color=DEFAULT_COLORS[i],
            name=DEFAULT_BODY_NAMES[i],
        )
        for i in range(3)
    ]


def _compute_accelerations(
    positions: np.ndarray,
    masses: np.ndarray,
    epsilon: float = SOFTENING_PARAMETER,
) -> np.ndarray:
    """
    Calcule les accélérations gravitationnelles pour chaque corps.

    Utilise un paramètre d'adoucissement (softening) pour éviter les singularités
    lorsque les corps sont très proches.

    Args:
        positions: Positions des corps, shape (n_bodies, 2)
        masses: Masses des corps, shape (n_bodies,)
        epsilon: Paramètre d'adoucissement pour stabilité numérique

    Returns:
        Accélérations des corps, shape (n_bodies, 2)
    """
    n_bodies = positions.shape[0]
    accelerations = np.zeros_like(positions)

    for i in range(n_bodies):
        # Vecteurs de distance entre le corps i et tous les autres
        diff = positions - positions[i]

        # Distance au carré avec softening
        dist_squared = np.sum(diff**2, axis=1) + epsilon**2
        dist_squared[i] = np.inf  # Éviter l'auto-interaction

        # Calcul de l'accélération gravitationnelle
        inv_dist_cubed = np.power(dist_squared, -1.5)
        accelerations[i] = GRAVITATIONAL_CONSTANT * np.sum(
            (masses[:, None] * diff) * inv_dist_cubed[:, None], axis=0
        )

        # Limiter l'accélération pour la stabilité numérique
        acc_magnitude = np.linalg.norm(accelerations[i])
        if acc_magnitude > MAX_ACCELERATION:
            accelerations[i] = accelerations[i] / acc_magnitude * MAX_ACCELERATION

    return accelerations


def simulate_three_body_attraction(
    total_time: float = DEFAULT_TOTAL_TIME,
    dt: float = DEFAULT_TIME_STEP,
    masses: List[float] | None = None,
    radii: List[float] | None = None,
    randomize: bool = False,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simule l'attraction gravitationnelle entre trois corps en 2D.

    Utilise l'intégrateur leap-frog (Verlet) pour une intégration symplectique,
    qui préserve mieux l'énergie du système sur de longues périodes.

    Args:
        total_time: Durée totale de la simulation (secondes)
        dt: Pas de temps pour l'intégration numérique
        masses: Masses des trois corps (optionnel)
        radii: Rayons des trois corps (optionnel)
        randomize: Active les perturbations aléatoires (False par défaut)

    Returns:
        times: Array des temps de simulation, shape (steps,)
        positions: Array des positions des corps, shape (steps, 3, 2)
    """
    # Créer les corps avec configuration initiale
    bodies = create_triangle_bodies(
        masses=masses,
        radii=radii,
        randomize=randomize,
    )

    # Initialiser les arrays de simulation
    n_bodies = len(bodies)
    steps = int(total_time / dt)
    times = np.linspace(0.0, total_time, steps)

    positions = np.zeros((steps, n_bodies, 2))
    velocities = np.zeros((n_bodies, 2))
    masses_arr = np.array([b.mass for b in bodies])

    # Conditions initiales
    positions[0] = np.array([b.position for b in bodies])
    velocities[:] = np.array([b.velocity for b in bodies])

    # Intégration leap-frog (Verlet)
    accelerations = _compute_accelerations(positions[0], masses_arr)

    for step in range(1, steps):
        # Demi-pas pour les vitesses
        velocities_half = velocities + 0.5 * accelerations * dt

        # Pas complet pour les positions
        positions[step] = positions[step - 1] + velocities_half * dt

        # Calcul des nouvelles accélérations
        accelerations_new = _compute_accelerations(positions[step], masses_arr)

        # Demi-pas final pour les vitesses
        velocities = velocities_half + 0.5 * accelerations_new * dt
        accelerations = accelerations_new

    return times, positions


__all__ = [
    "Body",
    "create_triangle_bodies",
    "simulate_three_body_attraction",
]
