"""
Bot Telegram pour les alertes en temps réel et le contrôle à distance de VodsTrade.
"""

import logging
import requests
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TelegramNotifier:
    """
    Gère l'envoi de notifications et de rapports via Telegram.
    """
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    def send_message(self, text: str, parse_mode: str = "Markdown"):
        """Envoie un message texte au chat configuré."""
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message Telegram : {e}")
            return False

    def notify_trade(self, trade_data: Dict[str, Any]):
        """Notifie l'exécution d'un trade."""
        emoji = "🚀" if trade_data['side'] == 'buy' else "📉"
        message = (
            f"{emoji} *Nouveau Trade Exécuté*\n\n"
            f"*Symbole :* `{trade_data['symbol']}`\n"
            f"*Côté :* `{trade_data['side'].upper()}`\n"
            f"*Prix :* `{trade_data['price']}`\n"
            f"*Quantité :* `{trade_data['amount']}`\n"
            f"*Exchange :* `{trade_data['exchange']}`\n"
            f"*Raison :* _{trade_data['reason']}_"
        )
        self.send_message(message)

    def notify_alert(self, level: str, message: str):
        """Envoie une alerte système (INFO, WARNING, CRITICAL)."""
        icons = {"INFO": "ℹ️", "WARNING": "⚠️", "CRITICAL": "🚨"}
        icon = icons.get(level.upper(), "🔔")
        formatted_message = f"{icon} *ALERTE {level.upper()}*\n\n{message}"
        self.send_message(formatted_message)

    def send_daily_report(self, report_data: Dict[str, Any]):
        """Envoie un rapport de performance quotidien."""
        message = (
            f"📊 *Rapport Quotidien VodsTrade*\n\n"
            f"*PnL 24h :* `{report_data['pnl_24h']}$` ({report_data['pnl_pct']}%)\n"
            f"*Trades :* `{report_data['total_trades']}`\n"
            f"*Taux de réussite :* `{report_data['win_rate']}%`\n"
            f"*Valeur Totale :* `{report_data['total_value']}$`"
        )
        self.send_message(message)
