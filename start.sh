#!/bin/bash

echo "🚀 VODSTRADE V9 - SÉQUENCE DE LANCEMENT"
echo "=========================================="
echo ""

# Vérification des prérequis
echo "📋 Vérification des prérequis..."

command -v docker >/dev/null 2>&1 || { echo "❌ Docker est requis"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose est requis"; exit 1; }

echo "✅ Prérequis OK"
echo ""

# Configuration
echo "🔧 Configuration de l'environnement..."
cp config/.env.example .env 2>/dev/null || true

# Création des dossiers nécessaires
mkdir -p logs data models

# Démarrage
echo "🐳 Démarrage des conteneurs Docker..."
docker-compose -f infra/docker-compose.yml up -d

# Attente du démarrage des services
echo "⏳ Attente du démarrage des services..."
sleep 10

# Vérification des services
echo "🔍 Vérification des services..."
curl -s http://localhost:8000/health > /dev/null && echo "✅ API OK" || echo "❌ Échec de l'API"
curl -s http://localhost:8501 > /dev/null && echo "✅ Dashboard OK" || echo "❌ Échec du Dashboard"

echo ""
echo "🎉 VODSTRADE V9 EST EN LIGNE !"
echo "==================================="
echo "📊 Dashboard : http://localhost:8501"
echo "🔧 Documentation API : http://localhost:8000/docs"
echo "📈 Monitoring : http://localhost:3000"
echo "🤖 n8n : http://localhost:5678"
echo ""
echo "⚠️  IMPORTANT : MODE PAPER TRADING ACTIF"
echo "   Pour activer le trading réel, modifiez le fichier .env et réglez PAPER_TRADING=false"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter"
