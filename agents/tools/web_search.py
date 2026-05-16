"""
Outils de recherche web pour les agents CrewAI de VodsTrade.
"""

from crewai_tools import tool
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class WebSearchTools:
    """
    Collection d'outils pour effectuer des recherches sur le web.
    """

    @tool("Recherche Internet")
    def search_internet(self, query: str) -> str:
        """
        Effectue une recherche sur Internet en utilisant un moteur de recherche.
        Utile pour obtenir des informations générales, des actualités ou des données spécifiques.
        """
        logger.info(f"Effectue une recherche Internet pour: {query}")
        try:
            # Utiliser une API de recherche web réelle ici (ex: Google Custom Search API, SerpApi)
            # Pour cet exemple, nous allons simuler une recherche simple avec DuckDuckGo
            url = f"https://duckduckgo.com/html/?q={query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            results = []
            for s in soup.find_all("a", class_="result__a"):
                results.append(s.get_text() + " - " + s["href"])
            
            if results:
                return "\n".join(results[:5]) # Retourne les 5 premiers résultats
            else:
                return "Aucun résultat trouvé pour la recherche."
        except Exception as e:
            logger.error(f"Erreur lors de la recherche Internet: {e}")
            return f"Erreur lors de la recherche Internet: {e}"
