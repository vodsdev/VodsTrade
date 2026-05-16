import asyncio
import logging
from config.settings import load_config
from core.engine import TradingEngine

# Configure logging
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
    logger.info("Démarrage de l'application VodsTrade...")
    config = load_config()
    engine = TradingEngine(config)
    await engine.start()
    
    # Keep the main loop running
    try:
        while True:
            await asyncio.sleep(3600) # Sleep for an hour or handle shutdown signals
    except asyncio.CancelledError:
        logger.info("Application VodsTrade arrêtée.")
    finally:
        await engine.stop()

if __name__ == "__main__":
    asyncio.run(main())
