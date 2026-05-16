"""
CrewAI pour l'analyse des médias sociaux.
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
import logging

from agents.base_agent import BaseAgent
from agents.tools.social_scraper import SocialScraperTools

logger = logging.getLogger(__name__)

class SocialMediaCrew(BaseAgent):
    """
    Agent CrewAI spécialisé dans l'analyse des médias sociaux pour VodsTrade.
    """
    def __init__(self, name: str, config: Dict):
        super().__init__(name, config)
        self.social_tools = SocialScraperTools()
        self.crew = self._create_crew()

    def _create_crew(self) -> Crew:
        """
        Crée et configure le CrewAI pour l'analyse des médias sociaux.
        """
        # Définition des agents
        social_analyst = Agent(
            role="Analyste de médias sociaux crypto",
            goal="Surveiller les plateformes de médias sociaux pour détecter les discussions influentes, les tendances virales et le sentiment de la communauté.",
            backstory="Expert en écoute sociale, capable d'identifier les signaux précoces de mouvements de marché basés sur l'activité des médias sociaux.",
            verbose=True,
            allow_delegation=False,
            tools=[self.social_tools.scrape_social_media]
        )

        # Définition des tâches
        task1 = Task(
            description="Collecter et analyser les discussions sur les principales plateformes de médias sociaux (Twitter, Reddit, Telegram) concernant les cryptomonnaies majeures.",
            expected_output="Un rapport sur les tendances des médias sociaux, les sujets populaires et le sentiment général de la communauté.",
            agent=social_analyst
        )

        return Crew(
            agents=[social_analyst],
            tasks=[task1],
            verbose=2,
            process=Process.sequential
        )

    async def analyze(self, market_data: Dict) -> Dict:
        """
        Exécute le CrewAI pour effectuer l'analyse des médias sociaux.
        """
        logger.info(f"Lancement de l'analyse des médias sociaux par l'agent {self.name}.")
        try:
            # Pour l'exemple, nous allons simuler des données d'entrée pour l'outil
            # Dans une vraie implémentation, market_data contiendrait les mots-clés à rechercher
            keywords = market_data.get("social_media_keywords", ["Bitcoin", "Ethereum", "crypto news"])
            result = self.crew.kickoff(inputs={"keywords": keywords})
            logger.info(f"Analyse des médias sociaux terminée par {self.name}.")
            return {"social_media_analysis_report": result}
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution du CrewAI d'analyse des médias sociaux: {e}")
            return {"error": str(e)}
