# notifications_free.py
# Notifiche gratis via Telegram/Discord webhook

import requests
import json

class FreeNotifier:
    """Notifiche gratis via webhook"""
    
    def __init__(self):
        self.telegram_bot_token = None  # Opzionale - crea bot gratis
        self.telegram_chat_id = None
        self.discord_webhook = None
        
    def setup_telegram(self, bot_token, chat_id):
        """Setup Telegram bot (gratis)"""
        self.telegram_bot_token = bot_token
        self.telegram_chat_id = chat_id
    
    def setup_discord(self, webhook_url):
        """Setup Discord webhook (gratis)"""
        self.discord_webhook = webhook_url
    
    def send_telegram(self, message):
        """Invia notifica Telegram"""
        if not self.telegram_bot_token:
            return
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            requests.post(url, json=data, timeout=5)
        except:
            pass
    
    def send_discord(self, message):
        """Invia notifica Discord"""
        if not self.discord_webhook:
            return
        
        try:
            data = {
                'content': message,
                'username': 'Promo Bot 2026'
            }
            requests.post(self.discord_webhook, json=data, timeout=5)
        except:
            pass
    
    def send_stats(self, stats):
        """Invia statistiche"""
        message = f"""
📊 <b>PROMO BOT STATS</b>
📝 Posts: {stats.get('posts', 0)}
✅ Success: {stats.get('success', 0)}
❌ Fails: {stats.get('fails', 0)}
🚫 Bans: {stats.get('bans', 0)}
📈 Rate: {stats.get('rate', 0)}%
        """
        
        self.send_telegram(message)
        self.send_discord(message)

# ==================== USAGE ====================
# notifier = FreeNotifier()
# notifier.setup_discord('https://discord.com/api/webhooks/your_webhook')
# notifier.send_stats(bot.stats)
