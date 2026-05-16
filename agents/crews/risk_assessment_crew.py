"""
CrewAI pour l'évaluation des risques.
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
import logging

from agents.base_agent import BaseAgent
# from agents.tools.risk_management_tools import RiskManagementTools # À implémenter si nécessaire

logger = logging.getLogger(__name__)

class RiskAssessmentCrew(BaseAgent):
    """
    Agent CrewAI spécialisé dans l'évaluation des risques pour VodsTrade.
    """
    def __init__(self, name: str, config: Dict):
        super().__init__(name, config)
        # self.risk_tools = RiskManagementTools() # Initialiser si des outils spécifiques sont nécessaires
        self.crew = self._create_crew()

    def _create_crew(self) -> Crew:
        """
        Crée et configure le CrewAI pour l'évaluation des risques.
        """
        # Définition des agents
        risk_analyst = Agent(
            role="Analyste de risques crypto",
            goal="Évaluer les risques potentiels associés aux stratégies de trading et aux conditions de marché.",
            backstory="Expert en gestion des risques financiers, capable d'identifier les vulnérabilités et de proposer des mesures d'atténuation.",
            verbose=True,
            allow_delegation=False,
            # tools=[self.risk_tools.assess_market_volatility] # Ajouter des outils si nécessaire
        )

        # Définition des tâches
        task1 = Task(
            description="Analyser les conditions actuelles du marché et les stratégies de trading proposées pour identifier les risques potentiels (volatilité, liquidité, risque de contrepartie).",
            expected_output="Un rapport d'évaluation des risques détaillant les menaces identifiées et les recommandations pour les atténuer.",
            agent=risk_analyst
        )

        return Crew(
            agents=[risk_analyst],
            tasks=[task1],
            verbose=2,
            process=Process.sequential
        )

    async def analyze(self, market_data: Dict) -> Dict:
        """
        Exécute le CrewAI pour effectuer l'évaluation des risques.
        """
        logger.info(f"Lancement de l'évaluation des risques par l'agent {self.name}.")
        try:
            # Pour l'exemple, nous allons simuler des données d'entrée pour l'outil
            # Dans une vraie implémentation, market_data contiendrait les données nécessaires à l'évaluation des risques
            result = self.crew.kickoff(inputs={
                "market_conditions": market_data.get("market_conditions", "volatilité élevée"),
                "proposed_strategies": market_data.get("proposed_strategies", "arbitrage de financement")
            })
            logger.info(f"Évaluation des risques terminée par {self.name}.")
            return {"risk_assessment_report": result}
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution du CrewAI d'évaluation des risques: {e}")
            return {"error": str(e)}
