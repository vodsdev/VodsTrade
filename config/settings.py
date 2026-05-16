"""
Configuration centrale du projet VodsTrade
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuration globale"""
    
    # Application
    APP_NAME = "VodsTrade V9"
    VERSION = "9.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Trading
    PAPER_TRADING = os.getenv("PAPER_TRADING", "True").lower() == "true"
    TRADING_INTERVAL = int(os.getenv("TRADING_INTERVAL", "10"))  # secondes
    SYMBOLS = os.getenv("SYMBOLS", "BTC/USDT,ETH/USDT,SOL/USDT,AVAX/USDT").split(",")
    
    # Risque
    MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "1000"))
    MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", "500"))
    MAX_LEVERAGE = int(os.getenv("MAX_LEVERAGE", "3"))
    
    # Fournisseurs LLM
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GROK_API_KEY = os.getenv("GROK_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
    
    # Exchanges
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
    BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
    BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")
    
    # Base de données
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/trading")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Agents
    AGENT_COUNT = int(os.getenv("AGENT_COUNT", "500"))
    MARKET_RESEARCH_AGENTS = int(os.getenv("MARKET_RESEARCH_AGENTS", "50"))
    SENTIMENT_AGENTS = int(os.getenv("SENTIMENT_AGENTS", "100"))
    TECHNICAL_AGENTS = int(os.getenv("TECHNICAL_AGENTS", "50"))
    FUNDAMENTAL_AGENTS = int(os.getenv("FUNDAMENTAL_AGENTS", "40"))
    ONCHAIN_AGENTS = int(os.getenv("ONCHAIN_AGENTS", "40"))
    NEWS_AGENTS = int(os.getenv("NEWS_AGENTS", "50"))
    SOCIAL_AGENTS = int(os.getenv("SOCIAL_AGENTS", "100"))
    RISK_AGENTS = int(os.getenv("RISK_AGENTS", "30"))
    STRATEGY_AGENTS = int(os.getenv("STRATEGY_AGENTS", "40"))
    EXECUTION_AGENTS = int(os.getenv("EXECUTION_AGENTS", "50"))
    
    # Modèles ML
    USE_GPU = os.getenv("USE_GPU", "True").lower() == "true"
    LSTM_HIDDEN_SIZE = int(os.getenv("LSTM_HIDDEN_SIZE", "128"))
    TRANSFORMER_LAYERS = int(os.getenv("TRANSFORMER_LAYERS", "3"))

settings = Settings()

def load_config():
    """Retourne la configuration sous forme de dictionnaire pour compatibilité"""
    return {
        "project_name": Settings.APP_NAME,
        "version": Settings.VERSION,
        "paper_trading": Settings.PAPER_TRADING,
        "trading_interval": Settings.TRADING_INTERVAL,
        "symbols": Settings.SYMBOLS,
        "risk": {
            "max_position_size": Settings.MAX_POSITION_SIZE,
            "max_daily_loss": Settings.MAX_DAILY_LOSS,
            "max_leverage": Settings.MAX_LEVERAGE
        },
        "agents": {
            "total_count": Settings.AGENT_COUNT,
            "market_research": Settings.MARKET_RESEARCH_AGENTS,
            "sentiment": Settings.SENTIMENT_AGENTS,
            "technical": Settings.TECHNICAL_AGENTS,
            "fundamental": Settings.FUNDAMENTAL_AGENTS,
            "onchain": Settings.ONCHAIN_AGENTS,
            "news": Settings.NEWS_AGENTS,
            "social": Settings.SOCIAL_AGENTS,
            "risk": Settings.RISK_AGENTS,
            "strategy": Settings.STRATEGY_AGENTS,
            "execution": Settings.EXECUTION_AGENTS
        },
        "ml": {
            "use_gpu": Settings.USE_GPU,
            "lstm_hidden_size": Settings.LSTM_HIDDEN_SIZE,
            "transformer_layers": Settings.TRANSFORMER_LAYERS
        }
    }
