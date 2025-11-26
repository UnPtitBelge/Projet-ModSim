#!/usr/bin/env python
"""
Point d’entrée de l’application Poincaré.
Exécute le serveur Dash.

Usage:
    python run.py
Optionnel:
    EXPORT FLASK_ENV=development (pour reloader)
"""

from src.app.app import create_app  # ou: from src.app import create_app (si API riche)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
