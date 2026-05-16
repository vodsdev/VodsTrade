"""
Stratégie de tenue de marché.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class MarketMaking:
    """
    Implémente une stratégie de tenue de marché (market making).
    """
    def __init__(self, config: Dict):
        self.config = config
        self.spread_tolerance = config.get("spread_tolerance", 0.001) # 0.1% du prix
        self.order_size = config.get("order_size", 0.001) # Taille de l'ordre en BTC
        logger.info("Stratégie de tenue de marché initialisée.")

    async def generate_signals(self, market_data: Dict) -> List[Dict]:
        """
        Génère des signaux de trading basés sur la stratégie de tenue de marché.
        """
        signals = []
        logger.info("Génération de signaux pour la tenue de marché...")

        # Exemple simplifié: placer des ordres bid et ask autour du prix actuel
        for symbol_key, ticker in market_data.get("tickers", {}).items():
            symbol = ticker.get("symbol")
            exchange = ticker.get("exchange")
            last_price = ticker.get("last")
            bid_price = ticker.get("bid")
            ask_price = ticker.get("ask")

            if symbol and exchange and last_price and bid_price and ask_price:
                # Calculer le prix d'achat et de vente pour le market making
                buy_price = last_price * (1 - self.spread_tolerance)
                sell_price = last_price * (1 + self.spread_tolerance)

                # Placer un ordre d'achat (bid)
                signals.append({
                    "symbol": symbol,
                    "side": "buy",
                    "amount": self.order_size,
                    "price": buy_price,
                    "exchange": exchange,
                    "order_type": "limit",
                    "reason": f"Market Making: Placer un ordre d'achat à {buy_price:.2f}"
                })

                # Placer un ordre de vente (ask)
                signals.append({
                    "symbol": symbol,
                    "side": "sell",
                    "amount": self.order_size,
                    "price": sell_price,
                    "exchange": exchange,
                    "order_type": "limit",
                    "reason": f"Market Making: Placer un ordre de vente à {sell_price:.2f}"
                })

        logger.info(f"Génération de signaux pour la tenue de marché terminée. {len(signals)} signaux générés.")
        return signals
