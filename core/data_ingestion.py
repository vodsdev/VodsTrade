"""
Gestionnaire d'ingestion de données de marché
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd

from .exchange_manager import ExchangeManager

logger = logging.getLogger(__name__)

class DataIngestion:
    """
    Gère l'ingestion de données de marché historiques et en temps réel.
    """
    
    def __init__(self, config: Dict, exchange_manager: ExchangeManager):
        self.config = config
        self.exchange_manager = exchange_manager
        self.historical_data_cache = {}
        self.realtime_data_stream = None # À implémenter avec websockets
        
    async def get_historical_data(self, exchange_name: str, symbol: str, timeframe: str, limit: int = 100) -> Optional[pd.DataFrame]:
        """Récupère les données historiques (OHLCV) pour un symbole donné."""
        exchange = self.exchange_manager.exchanges.get(exchange_name)
        if not exchange:
            logger.error(f"Exchange {exchange_name} non initialisé pour les données historiques.")
            return None
            
        cache_key = f"{exchange_name}_{symbol}_{timeframe}_{limit}"
        if cache_key in self.historical_data_cache:
            return self.historical_data_cache[cache_key]
            
        try:
            ohlcv = await asyncio.to_thread(
                exchange.fetch_ohlcv, self.exchange_manager._format_symbol(exchange_name, symbol), timeframe, limit=limit
            )
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)
            self.historical_data_cache[cache_key] = df
            return df
        except Exception as e:
            logger.error(f"Échec de la récupération des données historiques pour {symbol} sur {exchange_name}: {e}")
            return None
            
    async def get_realtime_data(self, exchange_name: str, symbol: str) -> Optional[Dict]:
        """Récupère les données en temps réel (ticker) pour un symbole donné."""
        return await self.exchange_manager.get_ticker(exchange_name, symbol)
        
    async def get_all_market_data(self) -> Dict:
        """Récupère toutes les données de marché nécessaires pour le trading."""
        market_data = {
            "tickers": {},
            "order_books": {},
            "historical": {}
        }
        
        # Récupérer les tickers en temps réel
        ticker_tasks = []
        for exchange_name in self.exchange_manager.exchanges.keys():
            for symbol in self.config.get("symbols", []):
                ticker_tasks.append(self.exchange_manager.get_ticker(exchange_name, symbol))
        
        tickers = await asyncio.gather(*ticker_tasks)
        for ticker in tickers:
            if ticker:
                market_data["tickers"][f"{ticker["symbol"]}_{ticker["exchange"]}"] = ticker
                
        # Récupérer les carnets d'ordres
        order_book_tasks = []
        for exchange_name in self.exchange_manager.exchanges.keys():
            for symbol in self.config.get("symbols", []):
                order_book_tasks.append(self.exchange_manager.get_order_book(exchange_name, symbol))
                
        order_books = await asyncio.gather(*order_book_tasks)
        for ob in order_books:
            if ob:
                market_data["order_books"][f"{ob["symbol"]}_{ob["exchange"]}"] = ob
                
        # Récupérer les données historiques (exemple pour un timeframe)
        historical_tasks = []
        for exchange_name in self.exchange_manager.exchanges.keys():
            for symbol in self.config.get("symbols", []):
                historical_tasks.append(self.get_historical_data(exchange_name, symbol, "1h", limit=100))
                
        historical_data = await asyncio.gather(*historical_tasks)
        for hd in historical_data:
            if hd is not None and not hd.empty:
                market_data["historical"][f"{hd.iloc[0].name}_{hd.iloc[0].name}"] = hd # Utiliser un nom plus significatif
                
        return market_data
