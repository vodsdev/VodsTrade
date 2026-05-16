"""
CrewAI pour l'analyse fondamentale.
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
import logging

from agents.base_agent import BaseAgent
from agents.tools.web_search import WebSearchTools

logger = logging.getLogger(__name__)

class FundamentalAnalysisCrew(BaseAgent):
    """
    Agent CrewAI spécialisé dans l'analyse fondamentale pour VodsTrade.
    """
    def __init__(self, name: str, config: Dict):
        super().__init__(name, config)
        self.web_search_tools = WebSearchTools()
        self.crew = self._create_crew()

    def _create_crew(self) -> Crew:
        """
        Crée et configure le CrewAI pour l'analyse fondamentale.
        """
        # Définition des agents
        fundamental_analyst = Agent(
            role="Analyste fondamental crypto",
            goal="Évaluer la valeur intrinsèque des cryptomonnaies en analysant les projets, les équipes, la technologie et l'adoption.",
            backstory="Expert en recherche approfondie, capable de décortiquer les whitepapers, les rapports financiers et les développements de projets.",
            verbose=True,
            allow_delegation=False,
            tools=[self.web_search_tools.search_internet]
        )

        # Définition des tâches
        task1 = Task(
            description="Effectuer une analyse fondamentale complète sur une cryptomonnaie donnée, en se concentrant sur son utilité, son équipe, sa feuille de route et sa communauté.",
            expected_output="Un rapport d'analyse fondamentale détaillé, incluant une évaluation de la valeur et des risques potentiels.",
            agent=fundamental_analyst
        )

        return Crew(
            agents=[fundamental_analyst],
            tasks=[task1],
            verbose=2,
            process=Process.sequential
        )

    async def analyze(self, market_data: Dict) -> Dict:
        """
        Exécute le CrewAI pour effectuer l'analyse fondamentale.
        """
        logger.info(f"Lancement de l'analyse fondamentale par l'agent {self.name}.")
        try:
            # Pour l'exemple, nous allons simuler des données d'entrée pour l'outil
            # Dans une vraie implémentation, market_data contiendrait le nom de la crypto à analyser
            crypto_name = market_data.get("crypto_to_analyze", "Ethereum")
            result = self.crew.kickoff(inputs={"crypto_name": crypto_name})
            logger.info(f"Analyse fondamentale terminée par {self.name}.")
            return {"fundamental_analysis_report": result}
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution du CrewAI d'analyse fondamentale: {e}")
            return {"error": str(e)}
