#!/bin/bash
# start.sh

echo "🚀 Avvio Promo Bot 2026 Free Edition"

# Avvia Xvfb per headless Chrome
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99

# Attesa per Xvfb
sleep 3

# Verifica Chrome
google-chrome --version
chromedriver --version

# Crea directory per sessioni
mkdir -p browser_sessions
mkdir -p logs
mkdir -p images
mkdir -p proxy_lists

# Avvia bot principale con logging
python ultimate_free_promoter.py 2>&1 | tee logs/bot_$(date +%Y%m%d_%H%M%S).log

echo "✅ Bot terminato"
