#!/bin/bash

# Script de déploiement pour VodsTrade

echo "Déploiement de VodsTrade..."

# Construire et démarrer les conteneurs Docker
docker-compose up --build -d

echo "VodsTrade déployé avec succès !"
