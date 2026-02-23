#!/usr/bin/env bash
# Exit on error
set -o errexit

# Installation des dépendances
pip install -r requirements.txt

# Collecte des fichiers statiques
python manage.py collectstatic --no-input

# Note: Les migrations seront exécutées manuellement après déploiement
# python manage.py migrate
