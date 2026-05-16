import asyncio
import logging
import os
from config.settings import load_config
from core.engine import TradingEngine
from core.security import SecurityManager

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("vodstrade.log")
    ]
)
logger = logging.getLogger(__name__)

async def main():
    print("\n🚀 VODSTRADE V10 - SYSTÈME DE TRADING INSTITUTIONNEL")
    print("==================================================\n")
    
    # --- VÉRIFICATION DE LA SÉCURITÉ ---
    api_key = os.getenv("VODSTRADE_API_KEY")
    try:
        SecurityManager.check_access(api_key)
    except SystemExit as e:
        # Message d'erreur déjà affiché par SecurityManager
        return

    logger.info("Démarrage de l'application VodsTrade...")
    config = load_config()
    engine = TradingEngine(config)
    await engine.start()
    
    # Boucle principale
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        logger.info("Application VodsTrade arrêtée.")
    finally:
        await engine.stop()

if __name__ == "__main__":
    asyncio.run(main())
