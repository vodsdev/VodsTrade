"""
Module Auto-ML pour l'optimisation automatique des hyperparamètres des modèles VodsTrade.
"""

import logging
from typing import Dict, Any, List
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

logger = logging.getLogger(__name__)

class AutoMLOptimizer:
    """
    Optimise automatiquement les modèles ML en cherchant les meilleurs paramètres.
    """
    def __init__(self):
        self.best_params = {}

    def optimize_random_forest(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """
        Cherche les meilleurs hyperparamètres pour un modèle Random Forest.
        """
        logger.info("Démarrage de l'optimisation Auto-ML pour Random Forest...")
        
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5, 10]
        }
        
        rf = RandomForestRegressor()
        grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=0)
        grid_search.fit(X, y)
        
        self.best_params = grid_search.best_params_
        logger.info(f"Meilleurs paramètres trouvés : {self.best_params}")
        
        return grid_search.best_estimator_
