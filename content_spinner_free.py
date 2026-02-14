# content_spinner_free.py
# Riscrive contenuti gratis per evitare duplicati

import random
import re
from collections import defaultdict

class FreeContentSpinner:
    """Spinner contenuti gratis - evita testi duplicati"""
    
    def __init__(self):
        # Sinonimi base
        self.synonyms = {
            'join': ['join', 'come to', 'enter', 'be part of', 'hop in', 'check out'],
            'awesome': ['awesome', 'amazing', 'incredible', 'fantastic', 'great', 'cool'],
            'community': ['community', 'group', 'server', 'family', 'hub', 'place'],
            'free': ['free', 'no cost', 'gratis', 'without payment', 'zero cost'],
            'best': ['best', 'top', 'greatest', 'finest', 'ultimate'],
            'new': ['new', 'fresh', 'recent', 'brand new', 'latest'],
            'now': ['now', 'today', 'right now', 'immediately', 'asap'],
            'click': ['click', 'press', 'hit', 'tap', 'select'],
            'link': ['link', 'url', 'invite', 'join link', 'access'],
            'game': ['game', 'gaming', 'play', 'multiplayer', 'gamer'],
            'discord': ['Discord', 'server', 'chat', 'voice chat'],
            'telegram': ['Telegram', 'group', 'channel', 'chat'],
            'members': ['members', 'people', 'users', 'gamers', 'folks'],
            'active': ['active', 'live', 'vibrant', 'engaged', 'busy'],
            'daily': ['daily', 'every day', 'regular', 'frequent'],
        }
        
        # Intro templates
        self.intros = [
            "Hey everyone!",
            "Hello there!", 
            "What's up guys?",
            "Hi fam!",
            "Greetings!",
            "Yo!",
            "Hey friends!",
            "Aloha!",
            "Howdy!",
            "Hey hey!"
        ]
        
        # Outros
        self.outros = [
            "See you there!",
            "Hope to see you!",
            "Come join us!",
            "Don't miss out!",
            "Be part of it!",
            "See you inside!",
            "Join the fun!",
            "Be awesome with us!"
        ]
        
    def spin_text(self, text):
        """Riscrivi testo completamente"""
        # Split in parole
        words = text.split()
        spun_words = []
        
        for word in words:
            word_clean = word.lower().strip('.,!?;:')
            
            if word_clean in self.synonyms:
                # Sostituisci con sinonimo
                synonym = random.choice(self.synonyms[word_clean])
                
                # Mantieni punteggiatura
                if word[-1] in '.,!?;:':
                    synonym += word[-1]
                
                # Mantieni capitalizzazione
                if word[0].isupper():
                    synonym = synonym.capitalize()
                
                spun_words.append(synonym)
            else:
                spun_words.append(word)
        
        return ' '.join(spun_words)
    
    def generate_post_variation(self, base_message, platform, niche):
        """Genera variazione di post"""
        intros = [
            f"🚀 {random.choice(self.intros)}",
            f"🎮 {random.choice(self.intros)}",
            f"💫 {random.choice(self.intros)}",
            f"✨ {random.choice(self.intros)}",
            f"🔥 {random.choice(self.intros)}",
        ]
        
        # Spin del testo base
        spun = self.spin_text(base_message)
        
        # Aggiungi elementi specifici piattaforma
        if platform == 'discord':
            platform_text = random.choice([
                f"Join our Discord server!",
                f"Discord community active now!",
                f"Come chat on Discord!",
            ])
        elif platform == 'telegram':
            platform_text = random.choice([
                f"Telegram group growing fast!",
                f"Join our Telegram channel!",
                f"Telegram community here!",
            ])
        else:
            platform_text = spun
        
        # Costruisci post
        post_parts = [
            random.choice(intros),
            platform_text,
            spun,
            random.choice(self.outros),
            random.choice(["🔥", "🚀", "💫", "✨", "🎉"]) * random.randint(1, 3)
        ]
        
        random.shuffle(post_parts)
        
        return ' '.join(post_parts)
    
    def generate_multiple_variations(self, base_message, count=10):
        """Genera multiple variazioni"""
        variations = []
        for i in range(count):
            var = self.generate_post_variation(base_message, random.choice(['discord', 'telegram']), 'gaming')
            variations.append(var)
        return variations

# ==================== USAGE ====================
spinner = FreeContentSpinner()
variations = spinner.generate_multiple_variations("Join our Discord server for gaming!", 5)
for v in variations:
    print(f"- {v}")
