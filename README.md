# Projet ModSim

## Installation locale de l'environnement

Ajouter un environnement virtuel python à la source

```bash
python3 -m venv <nom_environnement>
```

Installer les dépendances avec `pip`

```bash
pip install -r requirements.txt
```

Lancer l'application localement. Si nécessaire, suivre le tutoriel de la page officielle [Panel](https://panel.holoviz.org/getting_started/build_app.html)

```bash
panel serve app.py --autoreload --show
```
