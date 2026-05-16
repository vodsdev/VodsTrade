"""
Smart Order Routing (SOR) pour VodsTrade.
Optimise l'exécution des ordres en les répartissant sur plusieurs exchanges pour minimiser le slippage.
"""

import logging
from typing import Dict, List, Any
from core.exchange_manager import ExchangeManager

logger = logging.getLogger(__name__)

class SmartOrderRouter:
    """
    Routeur d'ordres intelligent pour obtenir le meilleur prix d'exécution.
    """
    def __init__(self, exchange_manager: ExchangeManager):
        self.exchange_manager = exchange_manager

    async def get_best_execution_plan(self, symbol: str, side: str, total_amount: float) -> List[Dict]:
        """
        Analyse la liquidité sur tous les exchanges disponibles et crée un plan d'exécution.
        """
        logger.info(f"Calcul du plan d'exécution SOR pour {total_amount} {symbol} ({side})...")
        
        execution_plan = []
        available_liquidity = []

        # 1. Récupérer les carnets d'ordres de tous les exchanges
        for exchange_name in self.exchange_manager.exchanges:
            try:
                order_book = await self.exchange_manager.get_order_book(exchange_name, symbol, limit=20)
                # On prend le prix et la quantité disponible
                # side 'buy' -> on regarde les 'asks' (vendeurs)
                # side 'sell' -> on regarde les 'bids' (acheteurs)
                entries = order_book['asks'] if side == 'buy' else order_book['bids']
                
                for price, amount in entries:
                    available_liquidity.append({
                        "exchange": exchange_name,
                        "price": price,
                        "amount": amount
                    })
            except Exception as e:
                logger.warning(f"Impossible de récupérer le carnet d'ordres pour {exchange_name} : {e}")

        # 2. Trier la liquidité par prix (croissant pour achat, décroissant pour vente)
        available_liquidity.sort(key=lambda x: x['price'], reverse=(side == 'sell'))

        # 3. Répartir l'ordre total sur les meilleures offres
        remaining_amount = total_amount
        for offer in available_liquidity:
            if remaining_amount <= 0:
                break
                
            fill_amount = min(remaining_amount, offer['amount'])
            execution_plan.append({
                "exchange": offer['exchange'],
                "price": offer['price'],
                "amount": fill_amount
            })
            remaining_amount -= fill_amount

        if remaining_amount > 0:
            logger.warning(f"Liquidité insuffisante pour remplir l'ordre total. Manquant : {remaining_amount}")

        return execution_plan

    async def execute_sor_order(self, symbol: str, side: str, total_amount: float):
        """Exécute le plan SOR."""
        plan = await self.get_best_execution_plan(symbol, side, total_amount)
        
        results = []
        for step in plan:
            logger.info(f"Exécution SOR : {step['amount']} sur {step['exchange']} à {step['price']}")
            # Appel réel à l'exchange (simulé ici)
            # result = await self.exchange_manager.create_order(step['exchange'], symbol, 'limit', side, step['amount'], step['price'])
            results.append(step)
            
        return results
