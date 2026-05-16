"""
Gestionnaire de pool d'agents pour orchestrer les agents CrewAI.
"""

import asyncio
import logging
from typing import Dict, List, Type

from .base_agent import BaseAgent
from .crews.market_research_crew import MarketResearchCrew
from .crews.sentiment_analysis_crew import SentimentAnalysisCrew
from .crews.technical_analysis_crew import TechnicalAnalysisCrew
from .crews.fundamental_analysis_crew import FundamentalAnalysisCrew
from .crews.onchain_analysis_crew import OnchainAnalysisCrew
from .crews.news_aggregator_crew import NewsAggregatorCrew
from .crews.social_media_crew import SocialMediaCrew
from .crews.risk_assessment_crew import RiskAssessmentCrew
from .crews.strategy_optimizer_crew import StrategyOptimizerCrew
from .crews.execution_crew import ExecutionCrew

logger = logging.getLogger(__name__)

class AgentPool:
    """
    Gère un pool d'agents CrewAI, leur démarrage, arrêt et coordination.
    """
    def __init__(self, config: Dict):
        self.config = config
        self.agents: Dict[str, BaseAgent] = {}
        self._initialize_agents()

    def _initialize_agents(self):
        """
        Initialise les agents basés sur la configuration.
        """
        agent_classes: Dict[str, Type[BaseAgent]] = {
            "market_research": MarketResearchCrew,
            "sentiment_analysis": SentimentAnalysisCrew,
            "technical_analysis": TechnicalAnalysisCrew,
            "fundamental_analysis": FundamentalAnalysisCrew,
            "onchain_analysis": OnchainAnalysisCrew,
            "news_aggregator": NewsAggregatorCrew,
            "social_media": SocialMediaCrew,
            "risk_assessment": RiskAssessmentCrew,
            "strategy_optimizer": StrategyOptimizerCrew,
            "execution": ExecutionCrew,
        }

        for agent_name, agent_class in agent_classes.items():
            if self.config.get(agent_name, {}).get("enabled", False):
                try:
                    self.agents[agent_name] = agent_class(agent_name, self.config[agent_name])
                    logger.info(f"Agent {agent_name} ajouté au pool.")
                except Exception as e:
                    logger.error(f"Échec de l'initialisation de l'agent {agent_name}: {e}")

    async def start_all(self):
        """
        Démarre tous les agents du pool.
        """
        tasks = [agent.start() for agent in self.agents.values()]
        await asyncio.gather(*tasks)
        logger.info("Tous les agents ont été démarrés.")

    async def stop_all(self):
        """
        Arrête tous les agents du pool.
        """
        tasks = [agent.stop() for agent in self.agents.values()]
        await asyncio.gather(*tasks)
        logger.info("Tous les agents ont été arrêtés.")

    async def analyze_market(self, market_data: Dict) -> Dict:
        """
        Demande à tous les agents d'analyser les données de marché.
        """
        results = await asyncio.gather(*[agent.analyze(market_data) for agent in self.agents.values()], return_exceptions=True)
        
        analysis_results = {}
        for i, agent_name in enumerate(self.agents.keys()):
            if not isinstance(results[i], Exception):
                analysis_results[agent_name] = results[i]
            else:
                logger.error(f"L'agent {agent_name} a échoué son analyse: {results[i]}")
        return analysis_results
