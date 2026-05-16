# VodsTrade V9 - Système de Trading IA Autonome 🚀

VodsTrade est une plateforme de trading de cryptomonnaies ultra-puissante et entièrement autonome. Elle utilise une architecture de **500 agents IA** (via CrewAI) collaborant en temps réel pour analyser, prédire et exécuter des stratégies de trading complexes.

## 🌟 Fonctionnalités Principales

- **Intelligence Collective** : 10 équipes (crews) spécialisées gérant 500 agents pour une analyse à 360° du marché.
- **Multi-LLM natif** : Routage intelligent entre OpenAI (GPT-4), Anthropic (Claude), Grok, Gemini, DeepSeek et NVIDIA.
- **Machine Learning Avancé** : Modèles LSTM, Transformer et Ensemble pour des prédictions de prix et de volatilité de haute précision.
- **Gestion des Risques Institutionnelle** : Calcul de VaR, CVaR, Stress Testing et Circuit Breaker automatique.
- **Dashboard Temps Réel** : Interface Streamlit élégante avec graphiques Plotly pour suivre vos performances et l'activité des agents.
- **Infrastructure GPU Ready** : Optimisé pour l'accélération matérielle via Docker et NVIDIA CUDA.

## 📦 Structure du Projet

| Dossier | Description |
| :--- | :--- |
| `core/` | Moteur de trading, gestion des exchanges et logique centrale. |
| `agents/` | Orchestration des 500 agents CrewAI et outils personnalisés. |
| `ml/` | Modèles prédictifs et logique d'apprentissage par renforcement. |
| `llm/` | Gestionnaires et routeurs pour les différents fournisseurs d'IA. |
| `strategies/` | Stratégies d'arbitrage, momentum, market making et retour à la moyenne. |
| `dashboard/` | Interface utilisateur web (Streamlit). |
| `infra/` | Configuration Docker, Nginx et déploiement. |
| `research/` | Outils de collecte de données (Web, Social, On-chain, News). |

## 🚀 Démarrage Rapide

### 1. Prérequis
- Docker et Docker Compose installés.
- Accès à un GPU NVIDIA (optionnel mais recommandé pour le ML).

### 2. Installation
```bash
git clone https://github.com/Maxthiba24/VodsTrade.git
cd VodsTrade
chmod +x start.sh
```

### 3. Configuration
Éditez le fichier `.env` (créé automatiquement au premier lancement ou à partir de `config/.env.example`) pour ajouter vos clés API :
- Exchanges (Binance, Bybit, OKX)
- LLM (OpenAI, Anthropic, etc.)

### 4. Lancement
```bash
./start.sh
```

## 📊 Monitoring
- **Dashboard** : [http://localhost:8501](http://localhost:8501)
- **API Docs** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **Automation (n8n)** : [http://localhost:5678](http://localhost:5678)

## ⚠️ Avertissement Légal
Le trading de cryptomonnaies comporte des risques substantiels. **VodsTrade** est un outil technologique fourni "tel quel". Commencez toujours en mode **PAPER_TRADING=true** pour tester vos stratégies sans risque financier.

---
Développé avec ❤️ pour la communauté des traders algorithmiques.
