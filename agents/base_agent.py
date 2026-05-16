"""
Classe de base pour tous les agents du système VodsTrade.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Classe abstraite de base pour définir l'interface commune de tous les agents.
    """
    def __init__(self, name: str, config: Dict):
        self.name = name
        self.config = config
        logger.info(f"Agent {self.name} initialisé.")

    @abstractmethod
    async def analyze(self, market_data: Dict) -> Dict:
        """
        Méthode abstraite pour l'analyse du marché par l'agent.
        Doit être implémentée par les sous-classes.
        """
        pass

    async def start(self):
        """
        Démarre l'agent. Peut être surchargée pour une logique de démarrage spécifique.
        """
        logger.info(f"Agent {self.name} démarré.")

    async def stop(self):
        """
        Arrête l'agent. Peut être surchargée pour une logique d'arrêt spécifique.
        """
        logger.info(f"Agent {self.name} arrêté.")
