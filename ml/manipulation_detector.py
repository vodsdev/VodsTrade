"""
Détecteur de manipulations de marché (Pump & Dump) basé sur l'IA pour VodsTrade.
"""

import numpy as np
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class ManipulationDetector:
    """
    Analyse les anomalies de volume et de prix pour détecter les manipulations.
    """
    def __init__(self, volume_threshold: float = 3.0, price_threshold: float = 0.05):
        self.volume_threshold = volume_threshold # Multiplicateur du volume moyen
        self.price_threshold = price_threshold   # Variation de prix rapide (5%)

    def analyze(self, ohlcv_data: List[List]) -> Dict[str, Any]:
        """
        Analyse les données OHLCV récentes pour détecter des signes de Pump & Dump.
        """
        if len(ohlcv_data) < 20:
            return {"is_manipulated": False, "confidence": 0.0}

        volumes = [x[5] for x in ohlcv_data]
        prices = [x[4] for x in ohlcv_data]

        avg_volume = np.mean(volumes[:-1])
        current_volume = volumes[-1]
        
        price_change = (prices[-1] - prices[-2]) / prices[-2]
        
        is_pump = (current_volume > avg_volume * self.volume_threshold) and (price_change > self.price_threshold)
        
        confidence = 0.0
        if is_pump:
            confidence = min(1.0, (current_volume / (avg_volume * self.volume_threshold)) * 0.5 + (price_change / self.price_threshold) * 0.5)
            logger.warning(f"⚠️ DÉTECTION DE PUMP POSSIBLE : Confiance {confidence*100:.2f}%")

        return {
            "is_manipulated": is_pump,
            "confidence": confidence,
            "type": "PUMP" if is_pump else "NORMAL",
            "metrics": {
                "volume_ratio": current_volume / avg_volume,
                "price_change": price_change
            }
        }
