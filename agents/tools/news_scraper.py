"""
Outils de scraping de nouvelles pour les agents CrewAI de VodsTrade.
"""

from crewai_tools import tool
import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class NewsScraperTools:
    """
    Collection d'outils pour scraper des nouvelles et articles.
    """

    @tool("Scraper les nouvelles")
    def scrape_news(self, query: str = "cryptocurrency news") -> List[Dict]:
        """
        Scrape les dernières nouvelles liées à une requête donnée.
        Retourne une liste de dictionnaires contenant le titre, l'URL et un extrait.
        """
        logger.info(f"Scraping des nouvelles pour: {query}")
        try:
            # Utiliser une API de nouvelles réelle ou un scraper plus robuste
            # Pour cet exemple, nous allons simuler un scraping simple
            url = f"https://news.google.com/search?q={query}&hl=fr&gl=FR&ceid=FR:fr"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            articles = []
            for item in soup.find_all("article", limit=5):
                title_tag = item.find("a", class_="DY5T1d R2RGF")
                link_tag = item.find("a", class_="DY5T1d R2RGF")
                snippet_tag = item.find("span", class_="xBbh9")

                title = title_tag.get_text() if title_tag else "N/A"
                link = "https://news.google.com" + link_tag["href"][1:] if link_tag and link_tag.get("href") else "N/A"
                snippet = snippet_tag.get_text() if snippet_tag else "N/A"
                
                articles.append({"title": title, "url": link, "snippet": snippet})
            
            if articles:
                return articles
            else:
                return [{"title": "Aucune nouvelle trouvée", "url": "N/A", "snippet": "N/A"}]
        except Exception as e:
            logger.error(f"Erreur lors du scraping des nouvelles: {e}")
            return [{"title": "Erreur de scraping", "url": "N/A", "snippet": str(e)}]
