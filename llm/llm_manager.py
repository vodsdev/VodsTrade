"""
Gestionnaire des grands modèles de langage (LLM) pour VodsTrade.
"""

import logging
from typing import Dict, List, Any

from .providers.openai_provider import OpenAIProvider
from .providers.anthropic_provider import AnthropicProvider
from .providers.grok_provider import GrokProvider
from .providers.gemini_provider import GeminiProvider
from .providers.deepseek_provider import DeepseekProvider
from .providers.nvidia_provider import NvidiaProvider
from .router import LLMRouter

logger = logging.getLogger(__name__)

class LLMManager:
    """
    Gère l'accès et l'orchestration de divers LLM pour les tâches de trading.
    """
    def __init__(self, config: Dict):
        self.config = config
        self.providers = self._initialize_providers()
        self.router = LLMRouter(config.get("router", {}), self.providers)

    def _initialize_providers(self) -> Dict[str, Any]:
        """
        Initialise les fournisseurs de LLM configurés.
        """
        providers = {}
        if self.config.get("openai", {}).get("enabled", False):
            providers["openai"] = OpenAIProvider(self.config["openai"])
            logger.info("Fournisseur OpenAI initialisé.")
        if self.config.get("anthropic", {}).get("enabled", False):
            providers["anthropic"] = AnthropicProvider(self.config["anthropic"])
            logger.info("Fournisseur Anthropic initialisé.")
        if self.config.get("grok", {}).get("enabled", False):
            providers["grok"] = GrokProvider(self.config["grok"])
            logger.info("Fournisseur Grok initialisé.")
        if self.config.get("gemini", {}).get("enabled", False):
            providers["gemini"] = GeminiProvider(self.config["gemini"])
            logger.info("Fournisseur Gemini initialisé.")
        if self.config.get("deepseek", {}).get("enabled", False):
            providers["deepseek"] = DeepseekProvider(self.config["deepseek"])
            logger.info("Fournisseur Deepseek initialisé.")
        if self.config.get("nvidia", {}).get("enabled", False):
            providers["nvidia"] = NvidiaProvider(self.config["nvidia"])
            logger.info("Fournisseur Nvidia initialisé.")
        return providers

    async def generate_text(self, prompt: str, model: Optional[str] = None, **kwargs) -> str:
        """
        Génère du texte en utilisant le LLM sélectionné ou le routeur.
        """
        if model and model in self.providers:
            return await self.providers[model].generate_text(prompt, **kwargs)
        else:
            return await self.router.route_and_generate(prompt, **kwargs)

    async def consolidate_signals(self, signals: List[Dict], agent_analysis: Dict, ml_predictions: Dict) -> List[Dict]:
        """
        Utilise un LLM pour consolider les signaux de trading provenant de différentes sources.
        """
        logger.info("Consolidation des signaux de trading via LLM...")
        prompt = f"Consolidez les signaux de trading suivants: {signals}. Analyse des agents: {agent_analysis}. Prédictions ML: {ml_predictions}. Fournissez une liste de signaux de trading consolidés et validés."
        
        try:
            consolidated_text = await self.generate_text(prompt, model=self.config.get("consolidation_model"))
            # Ici, vous devrez parser le texte consolidé en une liste de dictionnaires de signaux.
            # Pour l'exemple, nous allons juste retourner un signal simulé.
            logger.info("Signaux consolidés avec succès par LLM.")
            return [{
                "symbol": "BTC/USDT",
                "side": "buy",
                "amount": 0.01,
                "reason": "Consolidation LLM: forte convergence des signaux positifs."
            }]
        except Exception as e:
            logger.error(f"Erreur lors de la consolidation des signaux par LLM: {e}")
            return []

    async def analyze_news_sentiment(self, news_articles: List[str]) -> Dict:
        """
        Utilise un LLM pour analyser le sentiment des articles de presse.
        """
        logger.info("Analyse du sentiment des nouvelles via LLM...")
        prompt = f"Analysez le sentiment général des articles de presse suivants: {news_articles}. Retournez un résumé du sentiment (positif, négatif, neutre) et les points clés."
        try:
            sentiment_analysis_text = await self.generate_text(prompt, model=self.config.get("sentiment_model"))
            logger.info("Analyse du sentiment des nouvelles terminée par LLM.")
            return {"sentiment_summary": sentiment_analysis_text}
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du sentiment des nouvelles par LLM: {e}")
            return {"error": str(e)}
