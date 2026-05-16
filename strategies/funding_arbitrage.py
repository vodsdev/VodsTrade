"""
Stratégie d'arbitrage de financement.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class FundingArbitrage:
    """
    Implémente une stratégie d'arbitrage de financement.
    """
    def __init__(self, config: Dict):
        self.config = config
        self.min_spread = config.get("min_spread", 0.0005) # 0.05%
        self.max_position_size = config.get("max_position_size", 0.1) # % du capital
        logger.info("Stratégie d'arbitrage de financement initialisée.")

    async def generate_signals(self, funding_opportunities: Dict, ml_predictions: Dict) -> List[Dict]:
        """
        Génère des signaux de trading basés sur les opportunités d'arbitrage de financement.
        """
        signals = []
        logger.info("Génération de signaux pour l'arbitrage de financement...")

        for symbol, opportunities in funding_opportunities.items():
            # Exemple simplifié: si un spread suffisant est détecté
            if opportunities.get("spread", 0) > self.min_spread:
                # Intégrer les prédictions ML pour affiner la décision
                predicted_funding_rate = ml_predictions.get("funding_predictions", {}).get(symbol, 0)
                
                if predicted_funding_rate > 0: # Si le taux de financement prédit est positif, on peut short
                    signals.append({
                        "symbol": symbol,
                        "side": "sell", # Short le futur
                        "amount": self.max_position_size, # Taille de position simplifiée
                        "exchange": opportunities.get("exchange_future"),
                        "reason": f"Arbitrage de financement détecté avec spread de {opportunities['spread']:.4f} et prédiction positive."
                    })
                    signals.append({
                        "symbol": symbol,
                        "side": "buy", # Long le spot
                        "amount": self.max_position_size,
                        "exchange": opportunities.get("exchange_spot"),
                        "reason": f"Arbitrage de financement détecté avec spread de {opportunities['spread']:.4f} et prédiction positive."
                    })
                elif predicted_funding_rate < 0: # Si le taux de financement prédit est négatif, on peut long
                     signals.append({
                        "symbol": symbol,
                        "side": "buy", # Long le futur
                        "amount": self.max_position_size, # Taille de position simplifiée
                        "exchange": opportunities.get("exchange_future"),
                        "reason": f"Arbitrage de financement détecté avec spread de {opportunities['spread']:.4f} et prédiction négative."
                    })
                     signals.append({
                        "symbol": symbol,
                        "side": "sell", # Short le spot
                        "amount": self.max_position_size,
                        "exchange": opportunities.get("exchange_spot"),
                        "reason": f"Arbitrage de financement détecté avec spread de {opportunities['spread']:.4f} et prédiction négative."
                    })

        logger.info(f"Génération de signaux pour l'arbitrage de financement terminée. {len(signals)} signaux générés.")
        return signals
