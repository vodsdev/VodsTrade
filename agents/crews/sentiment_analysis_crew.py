"""
CrewAI pour l'analyse des sentiments.
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
import logging

from agents.base_agent import BaseAgent
from agents.tools.sentiment_analyzer import SentimentAnalyzerTools

logger = logging.getLogger(__name__)

class SentimentAnalysisCrew(BaseAgent):
    """
    Agent CrewAI spécialisé dans l'analyse des sentiments pour VodsTrade.
    """
    def __init__(self, name: str, config: Dict):
        super().__init__(name, config)
        self.sentiment_tools = SentimentAnalyzerTools()
        self.crew = self._create_crew()

    def _create_crew(self) -> Crew:
        """
        Crée et configure le CrewAI pour l'analyse des sentiments.
        """
        # Définition des agents
        sentiment_analyst = Agent(
            role="Analyste de sentiments crypto",
            goal="Analyser le sentiment général du marché à partir de diverses sources (actualités, réseaux sociaux).",
            backstory="Expert en traitement du langage naturel et en analyse de sentiments, capable de déchiffrer l'humeur du marché.",
            verbose=True,
            allow_delegation=False,
            tools=[self.sentiment_tools.analyze_text_sentiment]
        )

        # Définition des tâches
        task1 = Task(
            description="Collecter et analyser le sentiment des dernières actualités et discussions sur les réseaux sociaux concernant les cryptomonnaies majeures.",
            expected_output="Un rapport détaillé sur le sentiment du marché (positif, négatif, neutre) avec des scores de confiance.",
            agent=sentiment_analyst
        )

        return Crew(
            agents=[sentiment_analyst],
            tasks=[task1],
            verbose=2,
            process=Process.sequential
        )

    async def analyze(self, market_data: Dict) -> Dict:
        """
        Exécute le CrewAI pour effectuer l'analyse des sentiments.
        """
        logger.info(f"Lancement de l'analyse des sentiments par l'agent {self.name}.")
        try:
            # Pour l'exemple, nous allons simuler des données d'entrée pour l'outil
            # Dans une vraie implémentation, market_data contiendrait le texte à analyser
            sample_text = "Le marché crypto est en forte hausse aujourd'hui, les investisseurs sont très optimistes. Cependant, certains experts mettent en garde contre une correction imminente."
            result = self.crew.kickoff(inputs={'text_to_analyze': sample_text})
            logger.info(f"Analyse des sentiments terminée par {self.name}.")
            return {"sentiment_analysis_report": result}
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution du CrewAI d'analyse des sentiments: {e}")
            return {"error": str(e)}
