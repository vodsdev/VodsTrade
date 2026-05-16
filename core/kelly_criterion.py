"""
Module d'optimisation de la taille des positions via le Critère de Kelly.
Permet de maximiser la croissance du capital à long terme.
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class KellyCriterion:
    """
    Implémente le critère de Kelly pour la gestion dynamique de la taille des positions.
    """
    def __init__(self, fraction: float = 0.5):
        # On utilise souvent un "Kelly fractionnaire" (ex: 0.5) pour être plus conservateur
        self.fraction = fraction

    def calculate_position_size(self, win_rate: float, win_loss_ratio: float) -> float:
        """
        Calcule la fraction optimale du capital à investir.
        Formule : f* = (p * (b + 1) - 1) / b
        p = probabilité de gain (win_rate)
        b = ratio gain/perte (win_loss_ratio)
        """
        if win_loss_ratio <= 0:
            return 0.0
            
        p = win_rate
        q = 1 - p
        b = win_loss_ratio
        
        # Formule de Kelly
        kelly_f = (p * b - q) / b
        
        # Appliquer la fraction de Kelly (Kelly fractionnaire)
        final_f = kelly_f * self.fraction
        
        # S'assurer que la taille est positive et ne dépasse pas 100% du capital
        return max(0.0, min(final_f, 1.0))

    def get_optimal_allocation(self, strategy_performance: Dict[str, Any]) -> float:
        """
        Calcule l'allocation optimale basée sur les performances historiques d'une stratégie.
        """
        win_rate = strategy_performance.get("win_rate", 0.5)
        # Calcul du ratio win/loss moyen
        avg_win = strategy_performance.get("avg_win", 0.02)
        avg_loss = abs(strategy_performance.get("avg_loss", -0.01))
        
        win_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 1.0
        
        allocation = self.calculate_position_size(win_rate, win_loss_ratio)
        logger.info(f"Allocation Kelly calculée : {allocation*100:.2f}% (WinRate: {win_rate*100:.1f}%, Ratio: {win_loss_ratio:.2f})")
        return allocation
