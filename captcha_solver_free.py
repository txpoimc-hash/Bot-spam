# captcha_solver_free.py
# Risolutore captcha gratis (limitato ma funziona)

import requests
import base64
import time
import random
from io import BytesIO
from PIL import Image
import pytesseract  # Opzionale - OCR gratis

class FreeCaptchaSolver:
    """Risolutore captcha gratis"""
    
    def __init__(self):
        # Servizi captcha gratis
        self.free_services = [
            {
                'name': 'textcaptcha',
                'api': 'http://textcaptcha.com/api/1',
                'type': 'text'
            },
            {
                'name': '2captcha_demo',
                'api': 'https://2captcha.com/demo',
                'type': 'demo'
            }
        ]
        
        # OCR gratis (tesseract)
        self.use_ocr = False
        try:
            import pytesseract
            self.use_ocr = True
            print("[+] OCR disponibile per captcha semplici")
        except:
            print("[-] pytesseract non installato - captcha OCR non disponibile")
    
    def solve_text_captcha(self, image_data):
        """Risolvi captcha testuale con OCR"""
        if not self.use_ocr:
            return None
        
        try:
            img = Image.open(BytesIO(image_data))
            # Preprocessa immagine
            img = img.convert('L')  # Grayscale
            img = img.point(lambda x: 0 if x < 128 else 255)  # Binarize
            
            # OCR
            text = pytesseract.image_to_string(img, config='--psm 8').strip()
            return text
        except Exception as e:
            print(f"OCR error: {e}")
            return None
    
    def solve_recaptcha_free(self, site_key, url):
        """Tenta di risolvere reCAPTCHA gratis (funziona a volte)"""
        try:
            # Usa API demo di 2captcha
            response = requests.post(
                'https://2captcha.com/in.php',
                data={
                    'key': 'demo',  # Demo key
                    'method': 'userrecaptcha',
                    'googlekey': site_key,
                    'pageurl': url,
                    'json': 1
                }
            )
            
            if response.status_code == 200:
                request_id = response.json().get('request')
                
                # Poll per risultato
                for _ in range(30):
                    time.sleep(5)
                    result = requests.get(
                        'https://2captcha.com/res.php',
                        params={
                            'key': 'demo',
                            'action': 'get',
                            'id': request_id,
                            'json': 1
                        }
                    )
                    
                    if result.status_code == 200:
                        res_json = result.json()
                        if res_json.get('status') == 1:
                            return res_json.get('request')
                        elif 'CAPCHA_NOT_READY' in res_json.get('request', ''):
                            continue
                        else:
                            break
        except:
            pass
        
        return None
    
    def solve_hcaptcha_free(self, site_key, url):
        """Tenta di risolvere hCaptcha gratis"""
        # Implementa logica per hCaptcha se necessario
        return None

# ==================== USAGE ====================
# captcha_solver = FreeCaptchaSolver()
# solution = captcha_solver.solve_recaptcha_free('site_key', 'page_url')
