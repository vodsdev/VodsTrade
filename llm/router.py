"""
Routeur de LLM pour diriger les requêtes vers le LLM le plus approprié.
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class LLMRouter:
    """
    Décide quel LLM utiliser en fonction de la requête et des capacités des fournisseurs.
    """
    def __init__(self, config: Dict, providers: Dict[str, Any]):
        self.config = config
        self.providers = providers
        self.default_model = config.get("default_model", "openai")
        logger.info("Routeur LLM initialisé.")

    async def route_and_generate(self, prompt: str, **kwargs) -> str:
        """
        Route la requête vers le LLM le plus approprié et génère du texte.
        """
        # Logique de routage simplifiée: utilise le modèle par défaut
        # Une implémentation plus sophistiquée pourrait analyser le prompt
        # pour déterminer le meilleur LLM (ex: coût, performance, spécialisation).
        
        target_provider_name = self.default_model
        if target_provider_name not in self.providers:
            logger.warning(f"Fournisseur par défaut {target_provider_name} non trouvé. Utilisation du premier fournisseur disponible.")
            if not self.providers:
                logger.error("Aucun fournisseur LLM disponible.")
                return "Erreur: Aucun LLM disponible pour générer du texte."
            target_provider_name = list(self.providers.keys())[0]

        provider = self.providers[target_provider_name]
        logger.info(f"Routage de la requête vers le fournisseur LLM: {target_provider_name}")
        return await provider.generate_text(prompt, **kwargs)
