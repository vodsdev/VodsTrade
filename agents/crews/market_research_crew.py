"""
CrewAI pour la recherche de marché.
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
import logging

from agents.base_agent import BaseAgent
from agents.tools.web_search import WebSearchTools

logger = logging.getLogger(__name__)

class MarketResearchCrew(BaseAgent):
    """
    Agent CrewAI spécialisé dans la recherche de marché pour VodsTrade.
    """
    def __init__(self, name: str, config: Dict):
        super().__init__(name, config)
        self.web_search_tools = WebSearchTools()
        self.crew = self._create_crew()

    def _create_crew(self) -> Crew:
        """
        Crée et configure le CrewAI pour la recherche de marché.
        """
        # Définition des agents
        researcher = Agent(
            role="Analyste de recherche de marché",
            goal="Identifier les tendances du marché, les actualités et les événements qui pourraient affecter les prix des cryptomonnaies.",
            backstory="Expert en analyse de marché crypto, capable de dénicher des informations cruciales.",
            verbose=True,
            allow_delegation=False,
            tools=[self.web_search_tools.search_internet]
        )

        # Définition des tâches
        task1 = Task(
            description="Effectuer une recherche approfondie sur les dernières actualités et tendances du marché des cryptomonnaies.",
            expected_output="Un rapport concis sur les tendances actuelles et les événements majeurs.",
            agent=researcher
        )

        return Crew(
            agents=[researcher],
            tasks=[task1],
            verbose=2,
            process=Process.sequential
        )

    async def analyze(self, market_data: Dict) -> Dict:
        """
        Exécute le CrewAI pour effectuer la recherche de marché.
        """
        logger.info(f"Lancement de l'analyse de marché par l'agent {self.name}.")
        try:
            result = self.crew.kickoff()
            logger.info(f"Analyse de marché terminée par {self.name}.")
            return {"market_research_report": result}
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution du CrewAI de recherche de marché: {e}")
            return {"error": str(e)}
