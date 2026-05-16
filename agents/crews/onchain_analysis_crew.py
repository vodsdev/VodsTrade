"""
CrewAI pour l'analyse on-chain.
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
import logging

from agents.base_agent import BaseAgent
from agents.tools.onchain_analyzer import OnchainAnalyzerTools

logger = logging.getLogger(__name__)

class OnchainAnalysisCrew(BaseAgent):
    """
    Agent CrewAI spécialisé dans l'analyse on-chain pour VodsTrade.
    """
    def __init__(self, name: str, config: Dict):
        super().__init__(name, config)
        self.onchain_tools = OnchainAnalyzerTools()
        self.crew = self._create_crew()

    def _create_crew(self) -> Crew:
        """
        Crée et configure le CrewAI pour l'analyse on-chain.
        """
        # Définition des agents
        onchain_analyst = Agent(
            role="Analyste On-Chain",
            goal="Analyser les données de la blockchain pour identifier les mouvements significatifs des baleines, les flux d'échange et l'activité des contrats intelligents.",
            backstory="Expert en lecture de données blockchain, capable d'interpréter les transactions, les adresses et les métriques on-chain pour prédire les mouvements du marché.",
            verbose=True,
            allow_delegation=False,
            tools=[self.onchain_tools.get_whale_movements, self.onchain_tools.get_exchange_flows, self.onchain_tools.get_smart_contract_activity]
        )

        # Définition des tâches
        task1 = Task(
            description="Collecter et analyser les données on-chain pour Bitcoin et Ethereum, en se concentrant sur les transferts importants vers/depuis les exchanges et l'activité des grands détenteurs.",
            expected_output="Un rapport d'analyse on-chain détaillant les observations clés et leurs implications potentielles pour le marché.",
            agent=onchain_analyst
        )

        return Crew(
            agents=[onchain_analyst],
            tasks=[task1],
            verbose=2,
            process=Process.sequential
        )

    async def analyze(self, market_data: Dict) -> Dict:
        """
        Exécute le CrewAI pour effectuer l'analyse on-chain.
        """
        logger.info(f"Lancement de l'analyse on-chain par l'agent {self.name}.")
        try:
            # Pour l'exemple, nous allons simuler des données d'entrée pour l'outil
            # Dans une vraie implémentation, market_data contiendrait les cryptos à analyser
            crypto_symbols = market_data.get("onchain_symbols", ["BTC", "ETH"])
            result = self.crew.kickoff(inputs={"crypto_symbols": crypto_symbols})
            logger.info(f"Analyse on-chain terminée par {self.name}.")
            return {"onchain_analysis_report": result}
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution du CrewAI d'analyse on-chain: {e}")
            return {"error": str(e)}
