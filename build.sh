#!/usr/bin/env bash
# Exit on error
set -o errexit

# Installation des dépendances
pip install -r requirements.txt

# Collecte des fichiers statiques
python manage.py collectstatic --no-input

# ✅ Exécution automatique des migrations
python manage.py migrate

# Note: L'import des produits et la création du superutilisateur
# devront être faits une seule fois via l'interface admin
