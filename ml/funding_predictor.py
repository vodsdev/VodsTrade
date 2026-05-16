"""
Modèle de prédiction des taux de financement.
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class FundingPredictor:
    """
    Prédit les taux de financement futurs en utilisant des données historiques.
    """
    def __init__(self, config: Dict):
        self.config = config
        self.model = None
        self.model_path = config.get("model_path", "./ml/models/funding_predictor_model.joblib")

    def train_model(self, data: pd.DataFrame):
        """
        Entraîne le modèle de prédiction des taux de financement.
        Les données doivent contenir les colonnes nécessaires (ex: features, target).
        """
        logger.info("Entraînement du modèle de prédiction des taux de financement...")
        # Exemple simplifié: les 3 dernières colonnes sont des features, la dernière est la cible
        features = data.iloc[:, :-1]
        target = data.iloc[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        logger.info(f"Modèle de prédiction des taux de financement entraîné. MSE: {mse}")
        joblib.dump(self.model, self.model_path)
        logger.info(f"Modèle sauvegardé à: {self.model_path}")

    def load_model(self):
        """
        Charge un modèle de prédiction des taux de financement pré-entraîné.
        """
        try:
            self.model = joblib.load(self.model_path)
            logger.info(f"Modèle de prédiction des taux de financement chargé depuis: {self.model_path}")
        except FileNotFoundError:
            logger.warning(f"Modèle non trouvé à {self.model_path}. Veuillez l'entraîner d'abord.")
            self.model = None

    def predict(self, new_data: pd.DataFrame) -> List[float]:
        """
        Effectue des prédictions sur de nouvelles données.
        """
        if self.model is None:
            logger.error("Modèle non entraîné ou non chargé. Impossible de faire des prédictions.")
            return []
        
        logger.info("Effectue des prédictions avec le modèle de taux de financement...")
        predictions = self.model.predict(new_data)
        return predictions.tolist()
