"""
Gestionnaire de connexions WebSockets pour des données de marché en temps réel à basse latence.
"""

import asyncio
import json
import logging
import websockets
from typing import Dict, List, Callable, Any

logger = logging.getLogger(__name__)

class WebSocketManager:
    """
    Gère les flux de données en temps réel via WebSockets pour plusieurs exchanges.
    """
    def __init__(self):
        self.connections = {}
        self.handlers = {}
        self.is_running = False

    def register_handler(self, exchange: str, handler: Callable[[Dict], Any]):
        """Enregistre une fonction pour traiter les messages d'un exchange spécifique."""
        self.handlers[exchange] = handler

    async def connect(self, exchange: str, url: str, subscriptions: List[str]):
        """Établit une connexion WebSocket et s'abonne aux flux."""
        logger.info(f"Connexion WebSocket à {exchange} ({url})...")
        try:
            async with websockets.connect(url) as websocket:
                self.connections[exchange] = websocket
                
                # Envoi des messages d'abonnement
                for sub in subscriptions:
                    await websocket.send(json.dumps(sub))
                
                logger.info(f"Abonnements réussis pour {exchange}.")
                
                while self.is_running:
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    if exchange in self.handlers:
                        await self.handlers[exchange](data)
                        
        except Exception as e:
            logger.error(f"Erreur WebSocket pour {exchange} : {e}")
            # Tentative de reconnexion après un délai
            await asyncio.sleep(5)
            if self.is_running:
                await self.connect(exchange, url, subscriptions)

    async def start(self, config: Dict):
        """Démarre toutes les connexions configurées."""
        self.is_running = True
        tasks = []
        for exchange, settings in config.items():
            tasks.append(self.connect(exchange, settings['url'], settings['subscriptions']))
        await asyncio.gather(*tasks)

    async def stop(self):
        """Arrête toutes les connexions."""
        self.is_running = False
        for exchange, ws in self.connections.items():
            await ws.close()
        logger.info("Toutes les connexions WebSocket ont été fermées.")
