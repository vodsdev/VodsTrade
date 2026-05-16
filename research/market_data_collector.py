"""
Collecteur de données de marché pour la recherche.
"""

import logging
from typing import List, Dict, Any
from core.exchange_manager import ExchangeManager

logger = logging.getLogger(__name__)

class MarketDataCollector:
    """
    Collecte les données de marché (prix, volume, OHLCV) à partir des exchanges.
    """
    def __init__(self, config: Dict, exchange_manager: ExchangeManager):
        self.config = config
        self.exchange_manager = exchange_manager

    async def collect_ohlcv_data(self, exchange_name: str, symbol: str, timeframe: str = "1h", limit: int = 100) -> List[List[Any]]:
        """
        Collecte les données OHLCV (Open, High, Low, Close, Volume) pour un symbole et un intervalle de temps donnés.
        """
        logger.info(f"Collecte des données OHLCV pour {symbol} sur {exchange_name} ({timeframe}).")
        # Utilise l'ExchangeManager pour récupérer les données OHLCV
        ohlcv_data = await self.exchange_manager.exchanges[exchange_name].fetch_ohlcv(
            self.exchange_manager._format_symbol(exchange_name, symbol), timeframe, limit=limit
        )
        return ohlcv_data

    async def collect_ticker_data(self, exchange_name: str, symbol: str) -> Dict:
        """
        Collecte les données de ticker (prix actuel, bid, ask) pour un symbole donné.
        """
        logger.info(f"Collecte des données de ticker pour {symbol} sur {exchange_name}.")
        ticker_data = await self.exchange_manager.get_ticker(exchange_name, symbol)
        return ticker_data

    async def collect_order_book(self, exchange_name: str, symbol: str, limit: int = 20) -> Dict:
        """
        Collecte le carnet d'ordres pour un symbole donné.
        """
        logger.info(f"Collecte du carnet d'ordres pour {symbol} sur {exchange_name}.")
        order_book = await self.exchange_manager.get_order_book(exchange_name, symbol, limit=limit)
        return order_book
