"""
CrewAI pour l'optimisation des stratégies.
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
import logging

from agents.base_agent import BaseAgent
# from agents.tools.optimization_tools import OptimizationTools # À implémenter si nécessaire

logger = logging.getLogger(__name__)

class StrategyOptimizerCrew(BaseAgent):
    """
    Agent CrewAI spécialisé dans l'optimisation des stratégies pour VodsTrade.
    """
    def __init__(self, name: str, config: Dict):
        super().__init__(name, config)
        # self.optimization_tools = OptimizationTools() # Initialiser si des outils spécifiques sont nécessaires
        self.crew = self._create_crew()

    def _create_crew(self) -> Crew:
        """
        Crée et configure le CrewAI pour l'optimisation des stratégies.
        """
        # Définition des agents
        optimizer = Agent(
            role="Optimiseur de stratégies de trading",
            goal="Analyser les performances des stratégies existantes et proposer des améliorations pour maximiser les profits et minimiser les risques.",
            backstory="Expert en backtesting, optimisation de paramètres et modélisation de performance, capable de trouver les réglages optimaux.",
            verbose=True,
            allow_delegation=False,
            # tools=[self.optimization_tools.backtest_strategy] # Ajouter des outils si nécessaire
        )

        # Définition des tâches
        task1 = Task(
            description="Analyser les données de performance historiques des stratégies de trading et identifier les paramètres qui peuvent être ajustés pour améliorer la rentabilité et réduire le drawdown.",
            expected_output="Un rapport d'optimisation de stratégie avec des recommandations de paramètres et des projections de performance.",
            agent=optimizer
        )

        return Crew(
            agents=[optimizer],
            tasks=[task1],
            verbose=2,
            process=Process.sequential
        )

    async def analyze(self, market_data: Dict) -> Dict:
        """
        Exécute le CrewAI pour effectuer l'optimisation des stratégies.
        """
        logger.info(f"Lancement de l'optimisation des stratégies par l'agent {self.name}.")
        try:
            # Pour l'exemple, nous allons simuler des données d'entrée pour l'outil
            # Dans une vraie implémentation, market_data contiendrait les données de performance des stratégies
            result = self.crew.kickoff(inputs={
                "strategy_performance_data": market_data.get("strategy_performance_data", "données de performance simulées"),
                "strategy_name": market_data.get("strategy_name", "Funding Arbitrage")
            })
            logger.info(f"Optimisation des stratégies terminée par {self.name}.")
            return {"strategy_optimization_report": result}
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution du CrewAI d'optimisation des stratégies: {e}")
            return {"error": str(e)}
