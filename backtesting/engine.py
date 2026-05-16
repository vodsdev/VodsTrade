"""
Moteur de Backtesting Vectorisé de Haute Performance pour VodsTrade.
Utilise des calculs vectorisés pour simuler des stratégies sur de larges volumes de données.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Callable

logger = logging.getLogger(__name__)

class BacktestEngine:
    """
    Moteur de backtesting utilisant des opérations vectorisées pour une vitesse maximale.
    """
    def __init__(self, initial_capital: float = 10000.0, commission: float = 0.001):
        self.initial_capital = initial_capital
        self.commission = commission
        self.results = {}

    def run(self, data: pd.DataFrame, strategy_func: Callable, **kwargs) -> Dict[str, Any]:
        """
        Exécute un backtest sur un DataFrame de données historiques.
        Le DataFrame doit contenir au moins une colonne 'close'.
        """
        logger.info("Démarrage du backtest vectorisé...")
        df = data.copy()
        
        # Génération des signaux via la fonction de stratégie
        df['signal'] = strategy_func(df, **kwargs)
        
        # Calcul des positions (1 pour long, -1 pour short, 0 pour neutre)
        df['position'] = df['signal'].shift(1).fillna(0)
        
        # Calcul des rendements de l'actif
        df['market_returns'] = df['close'].pct_change()
        
        # Calcul des rendements de la stratégie
        df['strategy_returns'] = df['position'] * df['market_returns']
        
        # Prise en compte des commissions lors des changements de position
        df['trades'] = df['position'].diff().abs()
        df['strategy_returns'] -= df['trades'] * self.commission
        
        # Calcul de la courbe de capital cumulée
        df['cumulative_market_returns'] = (1 + df['market_returns']).cumprod()
        df['cumulative_strategy_returns'] = (1 + df['strategy_returns']).cumprod()
        
        # Calcul du capital final
        final_capital = self.initial_capital * df['cumulative_strategy_returns'].iloc[-1]
        
        # Calcul des métriques de performance
        total_return = (final_capital - self.initial_capital) / self.initial_capital
        sharpe_ratio = self._calculate_sharpe_ratio(df['strategy_returns'])
        max_drawdown = self._calculate_max_drawdown(df['cumulative_strategy_returns'])
        win_rate = self._calculate_win_rate(df['strategy_returns'])

        self.results = {
            "initial_capital": self.initial_capital,
            "final_capital": final_capital,
            "total_return": total_return,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "win_rate": win_rate,
            "equity_curve": df['cumulative_strategy_returns'].tolist()
        }
        
        logger.info(f"Backtest terminé. Rendement total : {total_return*100:.2f}%")
        return self.results

    def _calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calcule le ratio de Sharpe annualisé."""
        if returns.std() == 0:
            return 0.0
        # Hypothèse de 365 jours de trading pour la crypto
        avg_return = returns.mean() * 365
        std_dev = returns.std() * np.sqrt(365)
        return (avg_return - risk_free_rate) / std_dev

    def _calculate_max_drawdown(self, cumulative_returns: pd.Series) -> float:
        """Calcule le drawdown maximum."""
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        return drawdown.min()

    def _calculate_win_rate(self, returns: pd.Series) -> float:
        """Calcule le taux de réussite des trades."""
        positive_trades = returns[returns > 0].count()
        total_trades = returns[returns != 0].count()
        return positive_trades / total_trades if total_trades > 0 else 0.0
