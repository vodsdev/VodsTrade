"""
CrewAI pour l'exécution des ordres.
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, Any
import logging

from agents.base_agent import BaseAgent
from agents.tools.crypto_apis import CryptoAPITools

logger = logging.getLogger(__name__)

class ExecutionCrew(BaseAgent):
    """
    Agent CrewAI spécialisé dans l'exécution des ordres pour VodsTrade.
    """
    def __init__(self, name: str, config: Dict):
        super().__init__(name, config)
        self.crypto_api_tools = CryptoAPITools()
        self.crew = self._create_crew()

    def _create_crew(self) -> Crew:
        """
        Crée et configure le CrewAI pour l'exécution des ordres.
        """
        # Définition des agents
        executor = Agent(
            role="Exécuteur d'ordres de trading",
            goal="Exécuter les ordres de trading validés sur les exchanges de cryptomonnaies avec une efficacité maximale.",
            backstory="Expert en exécution d'ordres, capable de gérer les subtilités des API d'exchange, le slippage et la latence.",
            verbose=True,
            allow_delegation=False,
            tools=[self.crypto_api_tools.execute_trade]
        )

        # Définition des tâches
        task1 = Task(
            description="Recevoir un signal de trading validé et exécuter l'ordre correspondant sur l'exchange spécifié.",
            expected_output="Confirmation de l'exécution de l'ordre avec les détails de la transaction.",
            agent=executor
        )

        return Crew(
            agents=[executor],
            tasks=[task1],
            verbose=2,
            process=Process.sequential
        )

    async def analyze(self, market_data: Dict) -> Dict:
        """
        Exécute le CrewAI pour effectuer l'exécution des ordres.
        """
        logger.info(f"Lancement de l'exécution des ordres par l'agent {self.name}.")
        try:
            # Pour l'exemple, nous allons simuler un signal de trading
            # Dans une vraie implémentation, market_data contiendrait le signal validé
            sample_signal = {
                "exchange": "binance",
                "symbol": "BTC/USDT",
                "side": "buy",
                "amount": 0.001,
                "price": 60000
            }
            result = self.crew.kickoff(inputs={"trade_signal": sample_signal})
            logger.info(f"Exécution des ordres terminée par {self.name}.")
            return {"execution_report": result}
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution du CrewAI d'exécution des ordres: {e}")
            return {"error": str(e)}
