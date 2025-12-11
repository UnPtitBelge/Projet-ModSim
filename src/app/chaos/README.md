# Module Chaos - Problème à Trois Corps

Ce module implémente une simulation interactive du problème à trois corps, illustrant le comportement chaotique des systèmes dynamiques.

## Structure du module

### `constants.py`
Centralise toutes les constantes et paramètres de configuration :
- **Physique** : constante gravitationnelle, paramètres de stabilité numérique
- **Configuration des corps** : masses, rayons, couleurs par défaut, positions initiales
- **Simulation** : pas de temps, durée totale (30s), nombre de frames (300)
- **Visualisation** : styles d'animation, couleurs du thème
- **Perturbations** : facteur de randomisation pour explorer la sensibilité aux conditions initiales

### `simulation.py`
Implémente le modèle physique et l'intégration numérique :
- **`Body`** : Classe de données représentant un corps céleste
- **`create_triangle_bodies(randomize=False)`** : Crée la configuration initiale en triangle (non équilatéral) avec perturbations optionnelles (±5%)
- **`simulate_three_body_attraction()`** : Intègre numériquement les équations du mouvement avec l'algorithme leap-frog (Verlet)
- **`_compute_accelerations()`** : Calcule les accélérations gravitationnelles avec paramètre d'adoucissement

### `plots.py`
Génère les visualisations interactives Plotly :
- **`build_three_body_figure_with_data(randomize=False)`** : Crée l'animation complète avec retour des données
- **`build_three_body_figure()`** : Version simplifiée retournant uniquement la figure (déprécié)

### `callbacks.py`
Gère les interactions utilisateur via Dash :
- **`update_three_body_figure()`** : Génère une nouvelle simulation basée sur le bouton cliqué (Générer ou Reset)
- Utilise `ctx.triggered` pour distinguer les actions utilisateur
- Deux modes : perturbations aléatoires ou retour à la configuration de base

### `layout.py`
Construit l'interface utilisateur avec progression pédagogique :
- **Contexte historique** : Concours du roi Oscar II et découverte de Poincaré
- **Le problème à trois corps** : Section englobante avec simulation interactive, équations, et sensibilité
- **Comprendre le chaos** : Conclusion sur l'ordre dans le désordre, attracteurs étranges, et applications
- Utilise `alert_box("warning")` pour les avertissements utilisateur

## Fonctionnement

### Configuration initiale
Les trois corps sont positionnés en triangle (non équilatéral) avec coordonnées arrondies :
- Corps 1 (rouge) : (0, 2)
- Corps 2 (bleu) : (-2, -1)
- Corps 3 (vert) : (2, -1)

Masses asymétriques (1.0, 1.2, 0.8) favorisent l'émergence du chaos.

### Modes de simulation
- **Mode Reset** : Utilise les positions exactes définies dans `DEFAULT_POSITIONS`
- **Mode Générer** : Ajoute des perturbations aléatoires de ±5% aux positions initiales
- Permet d'observer la sensibilité aux conditions initiales caractéristique du chaos

### Intégration numérique
L'algorithme leap-frog (Verlet) est utilisé pour son caractère symplectique, préservant mieux l'énergie du système :
1. Demi-pas pour les vitesses
2. Pas complet pour les positions
3. Calcul des nouvelles accélérations
4. Demi-pas final pour les vitesses

### Stabilité numérique
- **Softening parameter (ε = 0.1)** : Évite les singularités quand les corps sont proches
- **Clamping d'accélération (max = 50.0)** : Limite l'accélération maximale pour prévenir les instabilités

### Animation
L'animation Plotly montre :
- Trajectoires accumulées pour chaque corps (avec opacité réduite)
- Position actuelle de chaque corps (marqueurs plus gros)
- Temps écoulé affiché dynamiquement
- Contrôles Play/Pause/Reset intégrés
- 300 frames sur 30 secondes (optimisé pour la performance)

### Loaders
- **Loader local** : Affiche un spinner pendant le calcul de la simulation (boutons Générer/Reset)
- Style cohérent avec le design system de l'application

## Personnalisation

Tous les paramètres peuvent être ajustés dans `constants.py` :
- Modifier les masses pour changer la dynamique
- Ajuster `DEFAULT_POSITIONS` pour changer la configuration de base
- Modifier `DEFAULT_RANDOMIZATION_FACTOR` (actuellement 0.05 = ±5%)
- Ajuster le pas de temps pour plus de précision
- Changer les couleurs et styles visuels
- Modifier la durée de simulation (`PLOT_TOTAL_TIME`)
- Ajuster le nombre de frames (`MAX_ANIMATION_FRAMES`)

## Notes techniques

- **Unités normalisées** : G = 1.0 simplifie les calculs
- **Sous-échantillonnage** : Limite à 300 frames pour les performances
- **Randomisation contrôlée** : Parameter `randomize` passé à travers toute la chaîne d'appels
- **Comportement chaotique** : Petites variations (±5%) → trajectoires radicalement différentes
- **Architecture callback** : Utilise `ctx.triggered` pour distinguer les boutons au lieu d'une logique de comptage
- **Design system** : Utilise `alert_box("warning")` pour les messages d'avertissement stylés
