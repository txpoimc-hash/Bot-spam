# robots_txt_bypass.py
# Bypassa robots.txt gratis

import urllib.robotparser

class RobotsTxtBypass:
    """Bypassa robots.txt intelligentemente"""
    
    def __init__(self):
        self.cache = {}
    
    def can_fetch(self, url, user_agent='*'):
        """Verifica se può fetchare - sempre True se vogliamo bypassare"""
        return True  # Ignora robots.txt
    
    def get_delay(self, url):
        """Ottieni delay raccomandato"""
        return 0  # Nessun delay

# Usa questo per ignorare robots.txt
robots_bypass = RobotsTxtBypass()
