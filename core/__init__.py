"""
VodsTrade - Module Core
"""

from .engine import TradingEngine
from .exchange_manager import ExchangeManager
from .risk_manager import RiskManager
from .data_ingestion import DataIngestion

__version__ = "9.0.0"
__all__ = ["TradingEngine", "ExchangeManager", "RiskManager", "DataIngestion"]
