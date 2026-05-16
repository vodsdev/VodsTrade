"""
Moteur de trading principal - Orchestrateur de tous les systèmes
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

from .exchange_manager import ExchangeManager
from .risk_manager import RiskManager
from .data_ingestion import DataIngestion
from agents.agent_pool import AgentPool
from strategies.funding_arbitrage import FundingArbitrage
from ml.ensemble_model import EnsemblePredictor
from llm.llm_manager import LLMManager

logger = logging.getLogger(__name__)

class TradingEngine:
    """
    Moteur central - Coordonne tous les composants
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.exchange_manager = ExchangeManager(config["exchanges"])
        self.risk_manager = RiskManager(config["risk"])
        self.data_ingestion = DataIngestion(config["data"])
        self.agent_pool = AgentPool(config["agents"])
        self.strategies = self._init_strategies()
        self.ml_predictor = EnsemblePredictor(config["ml"])
        self.llm_manager = LLMManager(config["llm"])
        
        self.is_running = False
        self.active_positions = {}
        
    def _init_strategies(self) -> Dict:
        """Initialise toutes les stratégies"""
        return {
            "funding_arbitrage": FundingArbitrage(self.config["strategies"]["funding"]),
            "pairs_trading": None,  # À implémenter
            "market_making": None,
            "momentum": None
        }
    
    async def start(self):
        """Démarre le moteur"""
        logger.info("🚀 Démarrage du moteur VodsTrade V9")
        
        # 1. Initialisation exchanges
        await self.exchange_manager.initialize_all()
        
        # 2. Démarrage agents IA
        await self.agent_pool.start_all()
        
        # 3. Chargement modèles ML
        await self.ml_predictor.load_models()
        
        # 4. Démarrage boucle principale
        self.is_running = True
        asyncio.create_task(self._main_loop())
        
    async def _main_loop(self):
        """Boucle principale de trading"""
        while self.is_running:
            try:
                # 1. Récupération données marché
                market_data = await self.data_ingestion.get_all_market_data()
                
                # 2. Analyse IA multi-agents
                agent_analysis = await self.agent_pool.analyze_market(market_data)
                
                # 3. Prédictions ML
                ml_predictions = await self.ml_predictor.predict(market_data)
                
                # 4. Génération signaux
                signals = await self._generate_signals(agent_analysis, ml_predictions)
                
                # 5. Validation risque
                validated_signals = await self.risk_manager.validate_signals(signals)
                
                # 6. Exécution
                for signal in validated_signals:
                    await self._execute_signal(signal)
                    
                # 7. Mise à jour positions
                await self._update_positions()
                
                # 8. Attente prochain cycle
                await asyncio.sleep(self.config["trading_interval"])
                
            except Exception as e:
                logger.error(f"Erreur boucle principale: {str(e)}")
                await asyncio.sleep(5)
    
    async def _generate_signals(self, agent_analysis: Dict, ml_predictions: Dict) -> List[Dict]:
        """Génère signaux de trading combinés"""
        signals = []
        
        # Stratégie Funding Arbitrage
        funding_signals = await self.strategies["funding_arbitrage"].generate_signals(
            agent_analysis.get("funding_opportunities", {}),
            ml_predictions.get("funding_predictions", {})
        )
        signals.extend(funding_signals)
        
        # Utilise LLM pour consolidation
        consolidated = await self.llm_manager.consolidate_signals(
            signals, agent_analysis, ml_predictions
        )
        
        return consolidated
    
    async def _execute_signal(self, signal: Dict) -> Dict:
        """Exécute un signal de trading"""
        try:
            # Vérification position existante
            if signal["symbol"] in self.active_positions:
                return {"status": "skipped", "reason": "position_exists"}
            
            # Exécution ordre
            order = await self.exchange_manager.execute_order(
                signal["exchange"],
                signal["symbol"],
                signal["side"],
                signal["size"]
            )
            
            if order and order.get("status") == "filled":
                self.active_positions[signal["symbol"]] = {
                    "entry_price": order["price"],
                    "size": signal["size"],
                    "side": signal["side"],
                    "timestamp": datetime.now(),
                    "signal": signal
                }
                
                # Notification
                await self._send_notification(f"Trade exécuté: {signal}")
                
            return order
            
        except Exception as e:
            logger.error(f"Erreur d'exécution du signal: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def _update_positions(self):
        """Met à jour les positions actives"""
        current_prices = await self.exchange_manager.get_all_prices()
        
        for symbol, position in list(self.active_positions.items()):
            current_price = current_prices.get(symbol)
            if current_price:
                pnl = (current_price - position["entry_price"]) * position["size"]
                if position["side"] == "sell":
                    pnl = -pnl
                    
                position["current_price"] = current_price
                position["pnl"] = pnl
                
                # Vérification stop loss
                if pnl <= -self.config["risk"]["max_loss_per_trade"]:
                    await self._close_position(symbol)
    
    async def _close_position(self, symbol: str):
        """Ferme une position"""
        position = self.active_positions.get(symbol)
        if position:
            opposite_side = "sell" if position["side"] == "buy" else "buy"
            await self.exchange_manager.execute_order(
                position.get("exchange", "binance"),
                symbol,
                opposite_side,
                position["size"]
            )
            del self.active_positions[symbol]
            await self._send_notification(f"Position fermée: {symbol}")
    
    async def _send_notification(self, message: str):
        """Envoie notification (Telegram, Discord, etc.)"""
        logger.info(f"NOTIFICATION: {message}")
        # Implémenter avec Telegram/Discord API
        
    async def stop(self):
        """Arrête le moteur"""
        self.is_running = False
        await self.agent_pool.stop_all()
        await self.exchange_manager.close_all()
        logger.info("🛑 Moteur de trading arrêté")
