"""
Module de sécurité pour la validation de la licence VodsTrade.
"""

import hashlib
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SecurityManager:
    # Le secret doit correspondre à celui utilisé dans VodsTrade-key
    MASTER_SECRET = "VODSTRADE_ULTIMATE_SECRET_2026"

    @staticmethod
    def validate_license(api_key: str) -> bool:
        """
        Vérifie la validité de la clé API fournie.
        """
        if not api_key:
            return False
            
        try:
            if not api_key.startswith("VT-"):
                return False
            
            parts = api_key[3:].split("-")
            if len(parts) != 2:
                return False
                
            raw_key, signature = parts
            
            # Vérifier la signature
            expected_signature = hashlib.sha256(f"{raw_key}:{SecurityManager.MASTER_SECRET}".encode()).hexdigest()[:16]
            if signature != expected_signature:
                return False
                
            # Vérifier l'expiration
            _, expiry_str, _ = raw_key.split(":")
            expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")
            
            if datetime.now() > expiry_date:
                logger.error("La clé API VodsTrade a expiré.")
                return False
                
            return True
        except Exception:
            return False

    @staticmethod
    def check_access(api_key: str):
        """
        Bloque l'exécution si la clé est invalide.
        """
        if not SecurityManager.validate_license(api_key):
            print("\n" + "="*50)
            print("❌ ERREUR DE SÉCURITÉ VODSTRADE")
            print("="*50)
            print("Aucune clé API valide détectée.")
            print("Vous devez créer votre clé API dans le dépôt VodsTrade-key.")
            print("Le système ne peut pas fonctionner sans licence valide.")
            print("="*50 + "\n")
            raise SystemExit("Accès refusé : Clé API manquante ou invalide.")
        
        logger.info("Licence VodsTrade validée avec succès.")
