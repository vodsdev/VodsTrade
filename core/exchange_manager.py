"""
Gestionnaire d'exchanges multi-plateformes avec rate limiting intelligent
"""

import ccxt
import asyncio
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from dataclasses import dataclass
import logging
from datetime import datetime
import random

logger = logging.getLogger(__name__)

@dataclass
class ExchangeCredentials:
    """Credentials sécurisés pour exchange"""
    api_key: str
    api_secret: str
    passphrase: Optional[str] = None

class ExchangeManager:
    """
    Gère tous les exchanges: Binance, Bybit, OKX, Kraken, Coinbase
    avec rate limiting, retries et fallback
    """
    
    SUPPORTED_EXCHANGES = ['binance', 'bybit', 'okx', 'kraken', 'coinbase']
    
    def __init__(self, config: Dict):
        self.config = config
        self.exchanges = {}
        self.markets_cache = {}
        self.order_books = {}
        self.rate_limiter = {}
        
    async def initialize_all(self):
        """Initialise tous les exchanges configurés"""
        tasks = []
        for exchange_name in self.SUPPORTED_EXCHANGES:
            if exchange_name in self.config.get('enabled', []):
                tasks.append(self.initialize_exchange(exchange_name))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Échec de l'initialisation de l'exchange: {result}")
                
        logger.info(f"Initialisé {len(self.exchanges)} exchanges")
        
    async def initialize_exchange(self, exchange_name: str) -> bool:
        """Initialise un exchange spécifique"""
        try:
            exchange_class = getattr(ccxt, exchange_name)
            
            credentials = self.config['credentials'].get(exchange_name, {})
            
            exchange_config = {
                'apiKey': credentials.get('api_key'),
                'secret': credentials.get('api_secret'),
                'enableRateLimit': True,
                'rateLimit': 1000,
                'options': {
                    'defaultType': 'future' if exchange_name in ['binance', 'bybit', 'okx'] else 'spot',
                    'adjustForTimeDifference': True
                }
            }
            
            if credentials.get('passphrase'):
                exchange_config['passphrase'] = credentials['passphrase']
                
            if self.config.get('testnet', True):
                exchange_config['sandbox'] = True
                
            exchange = exchange_class(exchange_config)
            
            # Test connection
            await asyncio.to_thread(exchange.load_markets)
            
            self.exchanges[exchange_name] = exchange
            self.rate_limiter[exchange_name] = asyncio.Semaphore(10)  # 10 requêtes simultanées max
            
            logger.info(f"✅ {exchange_name.upper()} initialisé")
            return True
            
        except Exception as e:
            logger.error(f"❌ Échec de l'initialisation de {exchange_name}: {str(e)}")
            return False
            
    async def get_ticker(self, exchange_name: str, symbol: str) -> Optional[Dict]:
        """Récupère le ticker avec retry"""
        exchange = self.exchanges.get(exchange_name)
        if not exchange:
            return None
            
        async with self.rate_limiter.get(exchange_name, asyncio.Semaphore(1)):
            for attempt in range(3):
                try:
                    ticker = await asyncio.to_thread(
                        exchange.fetch_ticker,
                        self._format_symbol(exchange_name, symbol)
                    )
                    return {
                        'symbol': symbol,
                        'bid': ticker.get('bid'),
                        'ask': ticker.get('ask'),
                        'last': ticker.get('last'),
                        'timestamp': ticker.get('timestamp'),
                        'datetime': ticker.get('datetime')
                    }
                except ccxt.NetworkError as e:
                    logger.warning(f"Erreur réseau lors de la récupération du ticker pour {symbol} sur {exchange_name} (tentative {attempt + 1}/3): {e}")
                    await asyncio.sleep(1)  # Attendre avant de réessayer
                except Exception as e:
                    logger.error(f"Erreur inattendue lors de la récupération du ticker pour {symbol} sur {exchange_name}: {e}")
                    break
            return None
            
    async def get_order_book(self, exchange_name: str, symbol: str, limit: int = 20) -> Optional[Dict]:
        """Récupère le carnet d'ordres"""
        exchange = self.exchanges.get(exchange_name)
        if not exchange:
            return None
            
        async with self.rate_limiter.get(exchange_name, asyncio.Semaphore(1)):
            try:
                order_book = await asyncio.to_thread(
                    exchange.fetch_order_book,
                    self._format_symbol(exchange_name, symbol),
                    limit
                )
                self.order_books[f"{exchange_name}_{symbol}"] = order_book
                return order_book
            except Exception as e:
                logger.error(f"Erreur lors de la récupération du carnet d'ordres pour {symbol} sur {exchange_name}: {e}")
                return None
                
    async def execute_order(self, exchange_name: str, symbol: str, side: str, amount: float, price: Optional[float] = None, order_type: str = 'market') -> Optional[Dict]:
        """Exécute un ordre de trading"""
        exchange = self.exchanges.get(exchange_name)
        if not exchange:
            logger.error(f"Exchange {exchange_name} non initialisé.")
            return None
            
        async with self.rate_limiter.get(exchange_name, asyncio.Semaphore(1)):
            try:
                if order_type == 'market':
                    order = await asyncio.to_thread(
                        exchange.create_market_order, self._format_symbol(exchange_name, symbol), side, amount
                    )
                elif order_type == 'limit' and price:
                    order = await asyncio.to_thread(
                        exchange.create_limit_order, self._format_symbol(exchange_name, symbol), side, amount, price
                    )
                else:
                    logger.error(f"Type d'ordre {order_type} non supporté ou prix manquant pour ordre limite.")
                    return None
                
                logger.info(f"Ordre exécuté sur {exchange_name}: {order}")
                return order
            except Exception as e:
                logger.error(f"Échec de l'exécution de l'ordre sur {exchange_name} pour {symbol}: {e}")
                return None
                
    async def get_balance(self, exchange_name: str, currency: Optional[str] = None) -> Optional[Dict]:
        """Récupère le solde du compte"""
        exchange = self.exchanges.get(exchange_name)
        if not exchange:
            return None
            
        async with self.rate_limiter.get(exchange_name, asyncio.Semaphore(1)):
            try:
                balance = await asyncio.to_thread(exchange.fetch_balance)
                if currency:
                    return balance['free'].get(currency)
                return balance
            except Exception as e:
                logger.error(f"Échec de la récupération du solde sur {exchange_name}: {e}")
                return None
                
    async def get_all_prices(self) -> Dict:
        """Récupère les derniers prix pour tous les symboles sur tous les exchanges"""
        all_prices = {}
        tasks = []
        for exchange_name, exchange in self.exchanges.items():
            tasks.append(self._fetch_exchange_prices(exchange_name, exchange))
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for res in results:
            if isinstance(res, dict):
                all_prices.update(res)
        return all_prices
        
    async def _fetch_exchange_prices(self, exchange_name: str, exchange) -> Dict:
        prices = {}
        async with self.rate_limiter.get(exchange_name, asyncio.Semaphore(1)):
            try:
                tickers = await asyncio.to_thread(exchange.fetch_tickers) # Ou fetch_ohlcv pour plus de données
                for symbol, ticker in tickers.items():
                    prices[symbol] = ticker['last']
            except Exception as e:
                logger.error(f"Échec de la récupération des prix sur {exchange_name}: {e}")
        return prices

    def _format_symbol(self, exchange_name: str, symbol: str) -> str:
        """Formate le symbole pour l'exchange spécifique"""
        # Exemple: 'BTC/USDT' pour Binance, 'BTC-USDT' pour Coinbase
        if exchange_name == 'coinbase':
            return symbol.replace('/', '-')
        return symbol
        
    async def close_all(self):
        """Ferme toutes les connexions aux exchanges"""
        for exchange_name, exchange in self.exchanges.items():
            try:
                # Certains exchanges peuvent avoir une méthode close ou logout
                # ccxt ne fournit pas de méthode universelle, donc on se contente de logger
                logger.info(f"Fermeture de la connexion pour {exchange_name}")
            except Exception as e:
                logger.error(f"Erreur lors de la fermeture de l'exchange {exchange_name}: {e}")
