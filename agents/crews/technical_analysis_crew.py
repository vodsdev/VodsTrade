"""
CrewAI pour l'analyse technique.
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
import logging

from agents.base_agent import BaseAgent
from agents.tools.technical_indicators import TechnicalIndicatorsTools

logger = logging.getLogger(__name__)

class TechnicalAnalysisCrew(BaseAgent):
    """
    Agent CrewAI spécialisé dans l'analyse technique pour VodsTrade.
    """
    def __init__(self, name: str, config: Dict):
        super().__init__(name, config)
        self.technical_tools = TechnicalIndicatorsTools()
        self.crew = self._create_crew()

    def _create_crew(self) -> Crew:
        """
        Crée et configure le CrewAI pour l'analyse technique.
        """
        # Définition des agents
        technical_analyst = Agent(
            role="Analyste technique crypto",
            goal="Appliquer des indicateurs techniques pour identifier les points d'entrée et de sortie potentiels.",
            backstory="Expert en lecture de graphiques et en utilisation d'indicateurs techniques comme le RSI, MACD, Bandes de Bollinger.",
            verbose=True,
            allow_delegation=False,
            tools=[self.technical_tools.calculate_rsi, self.technical_tools.calculate_macd, self.technical_tools.calculate_bollinger_bands]
        )

        # Définition des tâches
        task1 = Task(
            description="Analyser les données de prix historiques pour identifier les signaux d'achat/vente basés sur le RSI, MACD et les Bandes de Bollinger pour les cryptomonnaies majeures.",
            expected_output="Un rapport d'analyse technique détaillant les signaux identifiés et les niveaux de support/résistance.",
            agent=technical_analyst
        )

        return Crew(
            agents=[technical_analyst],
            tasks=[task1],
            verbose=2,
            process=Process.sequential
        )

    async def analyze(self, market_data: Dict) -> Dict:
        """
        Exécute le CrewAI pour effectuer l'analyse technique.
        """
        logger.info(f"Lancement de l'analyse technique par l'agent {self.name}.")
        try:
            # Pour l'exemple, nous allons simuler des données d'entrée pour l'outil
            # Dans une vraie implémentation, market_data contiendrait les données OHLCV
            sample_ohlcv = [
                [1678886400000, 20000, 20100, 19900, 20050, 100],
                [1678972800000, 20050, 20200, 20000, 20150, 120],
                [1679059200000, 20150, 20300, 20100, 20250, 150],
                [1679145600000, 20250, 20400, 20200, 20350, 130],
                [1679232000000, 20350, 20500, 20300, 20450, 160],
            ]
            result = self.crew.kickoff(inputs={'ohlcv_data': sample_ohlcv})
            logger.info(f"Analyse technique terminée par {self.name}.")
            return {"technical_analysis_report": result}
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution du CrewAI d'analyse technique: {e}")
            return {"error": str(e)}
