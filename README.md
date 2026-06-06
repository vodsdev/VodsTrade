# VodsTrade - Agents IA

Système d'agents IA pour l'analyse et l'exécution automatique de trades.

## Agents Disponibles

1. **Market Analyzer** - Analyse les tendances du marché
2. **Risk Manager** - Gère les risques et la taille des positions
3. **Portfolio Optimizer** - Optimise l'allocation du portefeuille
4. **Sentiment Analyzer** - Analyse le sentiment du marché
5. **Technical Analyst** - Effectue l'analyse technique
6. **Fundamental Analyst** - Analyse fondamentale
7. **Execution Agent** - Exécute les trades
8. **Monitoring Agent** - Monitore les positions
9. **Reporting Agent** - Génère les rapports
10. **Learning Agent** - Améliore continuellement les stratégies

## Architecture

Basé sur CrewAI avec intégration LLM complète.

## Utilisation

```python
from agents import TradingCrew
crew = TradingCrew()
results = crew.run()
```
