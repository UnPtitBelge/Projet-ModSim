# Guide de publication - Projet ModSim

Ce guide vous explique comment publier l'application Projet-ModSim en ligne.

---

## 📋 Prérequis

Avant de publier, assurez-vous que:

1. ✅ L'application fonctionne localement: `python run.py`
2. ✅ Tous les tests passent: `pytest`
3. ✅ Les dépendances sont listées: `requirements.txt` à jour
4. ✅ Le code est propre et documenté (refactoring terminé)
5. ✅ Git est configuré et le code commité

---

## 🚀 Options de déploiement

### 1. **Heroku** (Simple, gratuit/payant, recommandé pour Dash)

#### Avantages
- Déploiement facile avec Git push
- Logs centralisés
- Auto-scaling disponible
- Support Python natif

#### Étapes

**A. Créer un compte Heroku**
```bash
# 1. Créer un compte gratuit sur https://www.heroku.com
# 2. Installer Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
heroku login
```

**B. Préparer le projet**

```bash
# Créer Procfile (décrit comment lancer l'app)
echo "web: gunicorn run:server" > Procfile
```

Note: Dash utilise une variable `server` dans `app.py`. Modifiez `run.py`:

```python
# run.py
from src import create_app

app = create_app()
server = app.server  # Pour Gunicorn/Heroku

if __name__ == "__main__":
    app.run_server(debug=True)
```

**C. Ajouter Gunicorn aux dépendances**

```bash
pip install gunicorn
pip freeze > requirements.txt
```

**D. Déployer**

```bash
# Créer une app Heroku
heroku create nom-de-mon-app

# Déployer (Git push)
git push heroku main

# Voir les logs
heroku logs --tail

# Ouvrir l'app
heroku open
```

**Coûts Heroku:**
- Free tier: Pas de dyno actif après 30 min (app met en veille)
- Hobby: ~$7/mois (dyno toujours actif)
- Production: $25-500+/mois selon la charge

---

### 2. **PythonAnywhere** (Hosting Python dédié)

#### Avantages
- Spécialisé pour Python
- Interface web simple
- Plans abordables ($5-50/mois)

#### Étapes

**A. Créer un compte**
- Aller sur https://www.pythonanywhere.com
- Sign up gratuit ou payant

**B. Uploader le code**
- Web console: uploader le projet
- Ou Git: cloner depuis GitHub

**C. Configurer l'app web**
- Dashboard → Web → Add a new web app
- Choisir Python + Dash
- Pointer vers `run.py`

**D. Configurer WSGI**
- Éditer `/var/www/...wsgi.py`
- Ajouter les paths sys
- Importer et servir l'app

**Exemple wsgi.py:**
```python
import sys
path = '/home/your-username/your-project'
if path not in sys.path:
    sys.path.append(path)

from src import create_app

app = create_app()
```

**E. Recharger**
- Dashboard → Reload l'app web

---

### 3. **Railway** (Alternative Heroku, plus moderne)

#### Avantages
- Interface moderne
- Déploiement facile par Git
- Plans gratuit/payant
- Meilleur support que Heroku free tier

#### Étapes

**A. Créer un compte**
- https://railway.app

**B. Connecter GitHub**
- Autoriser Railway à accéder vos repos

**C. Créer un projet**
- New Project → Déployer depuis un repo Git
- Choisir la branche

**D. Configuration automatique**
- Railway détecte `requirements.txt`
- Configure l'app automatiquement
- Défini les variables d'environnement

**E. Déployer**
- Git push déclenche le déploiement auto
- Logs disponibles dans le dashboard

**Coûts Railway:**
- Gratuit: $5 de crédit mensuel
- Payant: Pay-as-you-go (~$0.50/jour pour une app simple)

---

### 4. **Render** (Alternative gratuite)

#### Avantages
- Free tier généreux
- Déploiement depuis Git
- SSL/HTTPS inclus

#### Étapes

**A. Créer un compte**
- https://render.com

**B. Créer un service web**
- New → Web Service
- Connecter GitHub repo

**C. Configurer**
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn run:server`
- Plan: Free

**D. Déployer**
- Render déploie auto à chaque push

**Limitations Free:**
- App se met en sommeil après 15 min d'inactivité
- Redémarrage lent

---

### 5. **DigitalOcean App Platform** (VPS simple)

#### Avantages
- Contrôle total
- Scaling facile
- Intégration GitHub

#### Étapes

**A. Créer un compte**
- https://www.digitalocean.com

**B. Créer une app**
- Apps → Create → Connect GitHub

**C. Configurer**
- Détecter automatiquement Python
- Définir port (8080)
- Build et start commands

**D. Déployer**
- Auto-déployment à chaque push

**Coûts:**
- À partir de $12/mois

---

## 📦 Préparation pour production

### 1. Configuration d'environnement

Créer un fichier `.env` (ne pas commiter!):

```bash
# .env
DEBUG=False
LOG_LEVEL=INFO
PORT=8080
```

Charger dans `run.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()
DEBUG = os.getenv("DEBUG", "False") == "True"
PORT = int(os.getenv("PORT", 8080))

app = create_app()
server = app.server

if __name__ == "__main__":
    app.run_server(debug=DEBUG, port=PORT, host="0.0.0.0")
```

### 2. Requirements.txt nettoyé

```bash
pip install pipreqs
pipreqs --force  # Générer requirements.txt auto
```

Ajouter les dépendances manquantes:

```
dash>=2.0.0
plotly>=5.0.0
numpy>=1.20.0
scipy>=1.7.0
gunicorn>=20.1.0
python-dotenv>=0.19.0
```

### 3. .gitignore

```
.venv
.env
logs/
*.pyc
__pycache__/
.pytest_cache/
*.egg-info/
dist/
build/
.DS_Store
```

### 4. README pour production

Ajouter une section au README:

```markdown
## Déploiement

### Déploiement sur Heroku

```bash
heroku create nom-app
git push heroku main
```

### Déploiement sur Railway

Pusher le code sur GitHub et connecter Railway.

### Logs

Vérifier les erreurs:
```bash
heroku logs --tail  # Heroku
# ou Dashboard → Logs pour Railway
```
```

---

## 🔒 Sécurité en production

### 1. Désactiver debug mode

```python
app.run_server(debug=False)
```

### 2. Ajouter des headers de sécurité

```python
@app.server.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

### 3. HTTPS obligatoire

La plupart des plateformes (Heroku, Railway, Render) offrent HTTPS gratuit.

### 4. Limiter les logs sensibles

Ne pas logger les données utilisateurs ou secrets:

```python
# ✅ Bon
log.info("User clicked zone %s", zone_type)

# ❌ Mauvais
log.info("Full user request: %s", request.data)
```

---

## 📊 Monitoring en production

### 1. Logs

Chaque plateforme a un dashboard de logs:

- **Heroku**: `heroku logs --tail`
- **Railway**: Dashboard → Logs
- **Render**: Dashboard → Logs

### 2. Health checks

Ajouter un endpoint de health:

```python
@app.server.route('/health')
def health():
    return {'status': 'ok'}, 200
```

### 3. Performance

- Utiliser le caching Dash pour les callbacks lourds
- Optimiser les figures Poincaré/phase
- Monitorer les erreurs avec un service (Sentry, etc.)

---

## ✅ Checklist avant production

- [ ] Application fonctionne localement
- [ ] Tous les tests passent
- [ ] requirements.txt à jour
- [ ] Pas d'importations de fichiers temporaires
- [ ] Debug mode désactivé
- [ ] Logs configurés (pas de données sensibles)
- [ ] .gitignore bien défini
- [ ] README mis à jour
- [ ] Code documenté et propre
- [ ] Secrets non commités (.env)
- [ ] HTTPS configuré
- [ ] Plateforme choisie et testée

---

## 🆘 Troubleshooting

### L'app plante au démarrage

1. Vérifier `requirements.txt` (toutes les dépendances listées?)
2. Vérifier les logs: `heroku logs --tail`
3. Essayer localement: `pip install -r requirements.txt && python run.py`

### Erreur 404 sur la page

- Vérifier les routes Dash (`@dash.register_page()`)
- Vérifier `dcc.Location(refresh=True)` configuration

### Lent au démarrage

- Figure Poincaré est coûteuse
- Ajouter un cache ou pré-générer au démarrage

### Erreurs de logs

- Ne pas oublier d'initialiser le logging
- Vérifier permissions pour `logs/` directory

---

## 📚 Ressources

- **Dash deployment**: https://dash.plotly.com/deployment
- **Heroku Python**: https://devcenter.heroku.com/articles/getting-started-with-python
- **Railway docs**: https://docs.railway.app/
- **Render docs**: https://render.com/docs/

---

## 🎯 Recommandation finale

**Pour un projet académique/prototype: Railway ou Render (gratuit)**
**Pour la production: Heroku Hobby tier ($7/mois) ou DigitalOcean ($12/mois)**

Railway offre le meilleur ratio gratuit/performance pour débuter.

