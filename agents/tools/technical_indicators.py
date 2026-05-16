"""
Outils d'indicateurs techniques pour les agents CrewAI de VodsTrade.
"""

from crewai_tools import tool
import pandas as pd
import ta
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TechnicalIndicatorsTools:
    """
    Collection d'outils pour calculer des indicateurs techniques.
    """

    def _prepare_dataframe(self, ohlcv_data: List[List[Any]]) -> pd.DataFrame:
        """
        Prépare un DataFrame Pandas à partir des données OHLCV.
        """
        df = pd.DataFrame(ohlcv_data, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df.set_index("timestamp")
        return df

    @tool("Calculer le RSI")
    def calculate_rsi(self, ohlcv_data: List[List[Any]], window: int = 14) -> Dict:
        """
        Calcule l'indice de force relative (RSI) pour les données OHLCV fournies.
        Retourne le dernier RSI calculé.
        """
        logger.info(f"Calcul du RSI avec une fenêtre de {window} pour les données OHLCV.")
        try:
            df = self._prepare_dataframe(ohlcv_data)
            df["rsi"] = ta.momentum.rsi(df["close"], window=window)
            return {"rsi": df["rsi"].iloc[-1], "window": window}
        except Exception as e:
            logger.error(f"Erreur lors du calcul du RSI: {e}")
            return {"error": str(e)}

    @tool("Calculer le MACD")
    def calculate_macd(self, ohlcv_data: List[List[Any]]) -> Dict:
        """
        Calcule la moyenne mobile de convergence et divergence (MACD) pour les données OHLCV fournies.
        Retourne les dernières valeurs MACD, signal et histogramme.
        """
        logger.info("Calcul du MACD pour les données OHLCV.")
        try:
            df = self._prepare_dataframe(ohlcv_data)
            df["macd"] = ta.trend.macd(df["close"])
            df["macd_signal"] = ta.trend.macd_signal(df["close"])
            df["macd_diff"] = ta.trend.macd_diff(df["close"])
            return {
                "macd": df["macd"].iloc[-1],
                "macd_signal": df["macd_signal"].iloc[-1],
                "macd_diff": df["macd_diff"].iloc[-1]
            }
        except Exception as e:
            logger.error(f"Erreur lors du calcul du MACD: {e}")
            return {"error": str(e)}

    @tool("Calculer les Bandes de Bollinger")
    def calculate_bollinger_bands(self, ohlcv_data: List[List[Any]], window: int = 20, window_dev: float = 2.0) -> Dict:
        """
        Calcule les Bandes de Bollinger pour les données OHLCV fournies.
        Retourne les dernières valeurs de la bande supérieure, moyenne et inférieure.
        """
        logger.info(f"Calcul des Bandes de Bollinger avec une fenêtre de {window} et déviation de {window_dev}.")
        try:
            df = self._prepare_dataframe(ohlcv_data)
            bollinger = ta.volatility.BollingerBands(df["close"], window=window, window_dev=window_dev)
            return {
                "bollinger_hband": bollinger.bollinger_hband().iloc[-1],
                "bollinger_mavg": bollinger.bollinger_mavg().iloc[-1],
                "bollinger_lband": bollinger.bollinger_lband().iloc[-1]
            }
        except Exception as e:
            logger.error(f"Erreur lors du calcul des Bandes de Bollinger: {e}")
            return {"error": str(e)}
