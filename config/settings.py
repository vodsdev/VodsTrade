import os

class Settings:
    PROJECT_NAME: str = "VodsTrade"
    PROJECT_VERSION: str = "9.0.0"

    # Configuration des exchanges
    EXCHANGES_CONFIG: dict = {
        "enabled": ["binance", "bybit"], # Activer les exchanges nécessaires
        "credentials": {
            "binance": {
                "api_key": os.getenv("BINANCE_API_KEY"),
                "api_secret": os.getenv("BINANCE_API_SECRET"),
            },
            "bybit": {
                "api_key": os.getenv("BYBIT_API_KEY"),
                "api_secret": os.getenv("BYBIT_API_SECRET"),
            },
        },
        "testnet": os.getenv("USE_TESTNET", "True").lower() == "true",
    }

    # Configuration des agents
    AGENTS_CONFIG: dict = {
        "market_research": {"enabled": True},
        "sentiment_analysis": {"enabled": True},
        "technical_analysis": {"enabled": True},
        "fundamental_analysis": {"enabled": True},
        "onchain_analysis": {"enabled": True},
        "news_aggregator": {"enabled": True},
        "social_media": {"enabled": True},
        "risk_assessment": {"enabled": True},
        "strategy_optimizer": {"enabled": True},
        "execution": {"enabled": True},
    }

    # Configuration des LLM
    LLM_CONFIG: dict = {
        "default_model": "openai", # Modèle par défaut pour le routage
        "openai": {
            "enabled": True,
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "gpt-4o-mini",
        },
        "anthropic": {
            "enabled": False,
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "model": "claude-3-opus-20240229",
        },
        "gemini": {
            "enabled": False,
            "api_key": os.getenv("GEMINI_API_KEY"),
            "model": "gemini-pro",
        },
        "grok": {
            "enabled": False,
            "api_key": os.getenv("GROK_API_KEY"),
            "model": "grok-1",
        },
        "deepseek": {
            "enabled": False,
            "api_key": os.getenv("DEEPSEEK_API_KEY"),
            "model": "deepseek-chat",
        },
        "nvidia": {
            "enabled": False,
            "api_key": os.getenv("NVIDIA_API_KEY"),
            "model": "nvidia-nemotron-4-340b-instruct",
        },
        "consolidation_model": "openai", # Modèle spécifique pour la consolidation des signaux
        "sentiment_model": "openai", # Modèle spécifique pour l'analyse de sentiment
    }

    # Configuration des stratégies
    STRATEGIES_CONFIG: dict = {
        "funding_arbitrage": {
            "enabled": True,
            "min_spread": 0.0005,
            "max_position_size": 0.1,
        },
        "pairs_trading": {"enabled": False, "threshold": 2.0},
        "market_making": {"enabled": False, "spread_tolerance": 0.001, "order_size": 0.001},
        "momentum": {"enabled": False, "momentum_period": 14, "entry_threshold": 0.02, "exit_threshold": -0.01},
        "mean_reversion": {"enabled": False, "window": 20, "std_dev_multiplier": 2.0},
    }

    # Configuration de la gestion des risques
    RISK_CONFIG: dict = {
        "max_exposure": 0.1, # 10% du capital
        "max_loss_per_trade": 0.01, # 1% du capital
        "max_daily_loss": 0.05, # 5% du capital
    }

    # Configuration de l'ingestion de données
    DATA_INGESTION_CONFIG: dict = {
        "symbols": ["BTC/USDT", "ETH/USDT"], # Symboles à surveiller
        "timeframes": ["1m", "5m", "1h", "1d"], # Intervalles de temps pour les données historiques
    }

    # Intervalle de trading (en secondes)
    TRADING_INTERVAL: int = 60 # Exécute la boucle principale toutes les 60 secondes

    # Chemins des modèles ML
    ML_MODELS_PATH: str = "./ml/models/"

    # Configuration du logging
    LOGGING_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "standard",
                "filename": "vodstrade.log",
                "maxBytes": 10485760, # 10 MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }


def load_config():
    return {
        "project_name": Settings.PROJECT_NAME,
        "project_version": Settings.PROJECT_VERSION,
        "exchanges": Settings.EXCHANGES_CONFIG,
        "agents": Settings.AGENTS_CONFIG,
        "llm": Settings.LLM_CONFIG,
        "strategies": Settings.STRATEGIES_CONFIG,
        "risk": Settings.RISK_CONFIG,
        "data": Settings.DATA_INGESTION_CONFIG,
        "trading_interval": Settings.TRADING_INTERVAL,
        "ml_models_path": Settings.ML_MODELS_PATH,
        "logging": Settings.LOGGING_CONFIG,
    }
