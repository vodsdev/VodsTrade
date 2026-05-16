# VodsTrade V9 - Système de Trading IA Complet

VodsTrade est un bot d'arbitrage de financement crypto professionnel, alimenté par l'IA, utilisant une architecture multi-agents CrewAI. Ce système intègre des modèles de langage (LLM) avancés, des prédictions de machine learning et une infrastructure robuste pour le trading automatisé.

## 📦 Structure du Projet

Le projet est organisé de la manière suivante :

- **`core/`** : Le moteur principal de trading, la gestion des exchanges et du risque.
- **`agents/`** : Orchestration des agents CrewAI et outils personnalisés.
- **`ml/`** : Modèles de machine learning pour les prédictions de prix, de financement et de volatilité.
- **`llm/`** : Gestion et routage vers divers fournisseurs de LLM (OpenAI, Anthropic, etc.).
- **`research/`** : Collecteurs de données web, sociales et on-chain.
- **`strategies/`** : Implémentations des stratégies de trading (Arbitrage, Momentum, etc.).
- **`dashboard/`** : Interface utilisateur basée sur Streamlit pour le suivi en temps réel.
- **`infra/`** : Configuration Docker et Nginx pour le déploiement.
- **`scripts/`** : Scripts utilitaires pour le déploiement et l'entraînement des modèles.
- **`config/`** : Paramètres de l'application et gestion des variables d'environnement.

## 🚀 Installation et Démarrage

### Prérequis

- Docker et Docker Compose
- Python 3.9+
- Clés API pour les exchanges et les fournisseurs de LLM

### Configuration

1.  Copiez le fichier `.env.example` vers `.env` dans le dossier `config/`.
2.  Remplissez vos clés API et configurez vos préférences.

### Lancement avec Docker

```bash
./scripts/deploy.sh
```

Cela démarrera le moteur de trading, le tableau de bord Streamlit et un serveur Redis.

## 🛠️ Fonctionnalités Clés

- **Multi-Agents CrewAI** : Plus de 10 agents spécialisés (recherche, sentiment, technique, etc.) collaborent pour analyser le marché.
- **Intégration LLM** : Utilisation de GPT-4, Claude, Grok et d'autres pour la consolidation des signaux et l'analyse de texte.
- **Machine Learning** : Prédictions basées sur des modèles Random Forest, Gradient Boosting et Apprentissage par Renforcement.
- **Arbitrage de Financement** : Stratégie optimisée pour capturer les écarts de taux de financement entre les exchanges.
- **Tableau de Bord Temps Réel** : Suivi des positions, des performances et des logs via une interface web intuitive.

## ⚖️ Avertissement de Risque

Le trading de cryptomonnaies comporte des risques élevés. VodsTrade est fourni à titre éducatif et technologique. Utilisez-le avec prudence et ne misez que ce que vous pouvez vous permettre de perdre.
