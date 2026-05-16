"""
Module de scraping web pour la collecte de données.
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class WebScraper:
    """
    Outil générique pour scraper des pages web.
    """
    def __init__(self, config: Dict = None):
        self.config = config if config is not None else {}
        self.headers = {
            "User-Agent": self.config.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        }

    def scrape_page(self, url: str) -> Optional[str]:
        """
        Scrape le contenu textuel d'une page web donnée.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Lève une exception pour les codes d'état HTTP d'erreur
            soup = BeautifulSoup(response.text, "html.parser")
            # Supprimer les scripts et les styles
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            # Supprimer les lignes vides et les espaces multiples
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for phrase in " ".join(lines).split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)
            logger.info(f"Page web scrapée avec succès: {url}")
            return text
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur de requête lors du scraping de {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erreur inattendue lors du scraping de {url}: {e}")
            return None

    def find_links(self, url: str, base_url: Optional[str] = None) -> List[str]:
        """
        Trouve tous les liens sur une page web donnée.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = []
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                if href.startswith("http") or href.startswith("https"):
                    links.append(href)
                elif base_url and href.startswith("/"):
                    links.append(base_url.rstrip("/") + href)
            logger.info(f"Liens trouvés sur {url}: {len(links)}")
            return links
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur de requête lors de la recherche de liens sur {url}: {e}")
            return []
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la recherche de liens sur {url}: {e}")
            return []
