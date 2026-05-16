"""
CrewAI pour l'agrégation de nouvelles.
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
import logging

from agents.base_agent import BaseAgent
from agents.tools.news_scraper import NewsScraperTools

logger = logging.getLogger(__name__)

class NewsAggregatorCrew(BaseAgent):
    """
    Agent CrewAI spécialisé dans l'agrégation de nouvelles pour VodsTrade.
    """
    def __init__(self, name: str, config: Dict):
        super().__init__(name, config)
        self.news_tools = NewsScraperTools()
        self.crew = self._create_crew()

    def _create_crew(self) -> Crew:
        """
        Crée et configure le CrewAI pour l'agrégation de nouvelles.
        """
        # Définition des agents
        news_aggregator = Agent(
            role="Agrégateur de nouvelles crypto",
            goal="Collecter les dernières nouvelles et articles pertinents sur le marché des cryptomonnaies.",
            backstory="Expert en veille médiatique, capable de filtrer le bruit et de trouver les informations les plus importantes.",
            verbose=True,
            allow_delegation=False,
            tools=[self.news_tools.scrape_news]
        )

        # Définition des tâches
        task1 = Task(
            description="Rechercher et agréger les nouvelles crypto les plus récentes et les plus influentes des dernières 24 heures.",
            expected_output="Un résumé des titres et des liens vers les articles de nouvelles les plus pertinents.",
            agent=news_aggregator
        )

        return Crew(
            agents=[news_aggregator],
            tasks=[task1],
            verbose=2,
            process=Process.sequential
        )

    async def analyze(self, market_data: Dict) -> Dict:
        """
        Exécute le CrewAI pour effectuer l'agrégation de nouvelles.
        """
        logger.info(f"Lancement de l'agrégation de nouvelles par l'agent {self.name}.")
        try:
            result = self.crew.kickoff()
            logger.info(f"Agrégation de nouvelles terminée par {self.name}.")
            return {"news_aggregation_report": result}
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution du CrewAI d'agrégation de nouvelles: {e}")
            return {"error": str(e)}
