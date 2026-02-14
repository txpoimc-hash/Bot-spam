# email_generator_free.py
# Genera email temporanee gratis per account throwaway

import requests
import random
import string
import time
import imaplib
import email
from bs4 import BeautifulSoup

class FreeEmailGenerator:
    """Generatore email temporanee completamente gratis"""
    
    def __init__(self):
        # Servizi email temporanee GRATIS
        self.email_services = [
            {
                'name': 'guerrillamail',
                'domain': 'guerrillamail.com',
                'api': 'https://api.guerrillamail.com/ajax.php',
                'type': 'api'
            },
            {
                'name': '10minutemail',
                'domain': '10minutemail.com',
                'api': 'https://10minutemail.net/address.api.php',
                'type': 'api'
            },
            {
                'name': 'temp-mail',
                'domain': 'temp-mail.org',
                'api': 'https://api.temp-mail.org/request/domains/format/json',
                'type': 'api'
            },
            {
                'name': 'mailinator',
                'domain': 'mailinator.com',
                'api': 'https://api.mailinator.com/api/domains',
                'type': 'api'
            },
            {
                'name': 'yopmail',
                'domain': 'yopmail.com',
                'api': None,
                'type': 'web'
            }
        ]
        
        # Domains gratuiti aggiuntivi
        self.free_domains = [
            '@yopmail.com',
            '@guerrillamail.com',
            '@10minutemail.com', 
            '@temp-mail.org',
            '@mailinator.com',
            '@trashmail.com',
            '@throwawaymail.com',
            '@spambox.us',
            '@discardmail.com',
            '@mailcatch.com',
            '@spamfree24.org',
            '@wegwerfmail.de',
            '@spamgourmet.com',
            '@mailnator.com',
            '@getnada.com',
            '@emailtemporanea.net',
            '@tempmail.net',
            '@fakeinbox.com',
            '@mailtemp.net',
            '@spamex.com'
        ]
        
    def generate_username(self, length=10):
        """Genera username casuale"""
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def get_random_domain(self):
        """Ottieni dominio casuale"""
        return random.choice(self.free_domains)
    
    def create_temp_email(self, service='random'):
        """Crea email temporanea"""
        if service == 'random':
            service = random.choice(list(self.email_services))
        
        username = self.generate_username()
        domain = self.get_random_domain().replace('@', '')
        
        email = f"{username}@{domain}"
        
        print(f"[+] Email creata: {email}")
        return {
            'email': email,
            'username': username,
            'domain': domain,
            'created': time.time(),
            'expires': time.time() + 600  # 10 minuti
        }
    
    def check_inbox_10minutemail(self, email):
        """Controlla inbox di 10minutemail"""
        try:
            username = email.split('@')[0]
            response = requests.get(
                f"https://10minutemail.net/messages.api.php",
                params={'email': email},
                timeout=10
            )
            if response.status_code == 200:
                return response.json().get('messages', [])
        except:
            pass
        return []
    
    def check_inbox_guerrillamail(self, email):
        """Controlla inbox guerrillamail"""
        try:
            session = requests.Session()
            # Ottieni sid
            sid_resp = session.get(
                "https://api.guerrillamail.com/ajax.php",
                params={'f': 'get_email_address'}
            ).json()
            
            # Controlla email
            check_resp = session.get(
                "https://api.guerrillamail.com/ajax.php",
                params={'f': 'fetch_email', 'sid': sid_resp.get('sid')}
            ).json()
            
            return check_resp.get('list', [])
        except:
            return []
    
    def wait_for_verification(self, email, service='10minutemail', timeout=300):
        """Aspetta email di verifica"""
        print(f"[*] In attesa di email di verifica per {email}...")
        
        start_time = time.time()
        check_interval = 5  # secondi
        
        while time.time() - start_time < timeout:
            if service == '10minutemail':
                messages = self.check_inbox_10minutemail(email)
            elif service == 'guerrillamail':
                messages = self.check_inbox_guerrillamail(email)
            else:
                time.sleep(check_interval)
                continue
            
            if messages:
                for msg in messages:
                    if 'verify' in msg.get('subject', '').lower() or 'confirm' in msg.get('subject', '').lower():
                        # Estrai link di verifica
                        verification_link = self.extract_verification_link(msg)
                        if verification_link:
                            print(f"[+] Link verifica trovato: {verification_link}")
                            return verification_link
            
            time.sleep(check_interval)
        
        print("[-] Timeout - nessuna email di verifica ricevuta")
        return None
    
    def extract_verification_link(self, message):
        """Estrai link di verifica dall'email"""
        # Implementa parsing HTML
        if 'html' in message:
            soup = BeautifulSoup(message['html'], 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if 'verify' in href or 'confirm' in href or 'activate' in href:
                    return href
        return None

# ==================== USAGE ====================
email_gen = FreeEmailGenerator()
temp_email = email_gen.create_temp_email()
print(f"Email temporanea: {temp_email['email']}")
