"""
Fonctions de génération de graphiques pour la page principale de stabilité.

Ce module peut contenir des fonctions supplémentaires de génération de graphiques
spécifiques à la page principale si nécessaire. Pour l'instant, il réexporte
les fonctions de base depuis base_figures.
"""

from ..base_figures import create_phase_diagram, create_system_graph

__all__ = ["create_system_graph", "create_phase_diagram"]
