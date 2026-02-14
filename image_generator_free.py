# image_generator_free.py
# Genera immagini uniche gratis per post (evita ban)

import requests
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import os
import numpy as np
import hashlib

class FreeImageGenerator:
    """Genera immagini uniche completamente gratis"""
    
    def __init__(self):
        # API immagini gratuite
        self.image_apis = [
            "https://picsum.photos/800/600",  # Random images
            "https://placekitten.com/800/600", # Kittens
            "https://place.dog/800/600",       # Dogs
            "https://api.lorem.space/image/game?w=800&h=600", # Gaming
            "https://api.lorem.space/image/movie?w=800&h=600", # Movies
            "https://api.lorem.space/image/album?w=800&h=600", # Music
        ]
        
        # Colori di sfondo
        self.background_colors = [
            (52, 152, 219),  # Blue
            (46, 204, 113),  # Green
            (155, 89, 182),  # Purple
            (52, 73, 94),    # Dark Blue
            (241, 196, 15),  # Yellow
            (230, 126, 34),  # Orange
            (231, 76, 60),   # Red
            (236, 240, 241), # Light Gray
            (149, 165, 166), # Gray
            (26, 188, 156),  # Turquoise
        ]
        
        # Overlay patterns
        self.patterns = ['dots', 'lines', 'grid', 'noise', 'gradient']
        
    def fetch_random_image(self):
        """Scarica immagine casuale gratis"""
        try:
            url = random.choice(self.image_apis)
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                img = Image.open(io.BytesIO(response.content))
                return img
        except:
            pass
        return None
    
    def generate_abstract_image(self, width=800, height=600):
        """Genera immagine astratta unica"""
        # Crea sfondo
        bg_color = random.choice(self.background_colors)
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Disegna forme casuali
        for _ in range(random.randint(5, 20)):
            shape_type = random.choice(['circle', 'rectangle', 'line'])
            color = tuple(random.randint(0, 255) for _ in range(3))
            
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(x1, width)
            y2 = random.randint(y1, height)
            
            if shape_type == 'circle':
                draw.ellipse([x1, y1, x2, y2], fill=color, outline=None)
            elif shape_type == 'rectangle':
                draw.rectangle([x1, y1, x2, y2], fill=color, outline=None)
            else:
                draw.line([x1, y1, x2, y2], fill=color, width=random.randint(1, 5))
        
        # Applica filtro casuale
        filters = [ImageFilter.BLUR, ImageFilter.CONTOUR, ImageFilter.EDGE_ENHANCE,
                  ImageFilter.EMBOSS, ImageFilter.SHARPEN, ImageFilter.SMOOTH]
        
        img = img.filter(random.choice(filters))
        
        return img
    
    def add_text_to_image(self, image, text):
        """Aggiungi testo all'immagine"""
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        # Prova a caricare font, altrimenti usa default
        try:
            font_size = random.randint(30, 60)
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
        except:
            font = ImageFont.load_default()
        
        # Posiziona testo al centro
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Colore testo (bianco o nero in base allo sfondo)
        text_color = (255, 255, 255)  # Bianco
        
        # Aggiungi ombra
        shadow_color = (0, 0, 0)
        for offset in range(2, 5):
            draw.text((x+offset, y+offset), text, font=font, fill=shadow_color)
        
        # Testo principale
        draw.text((x, y), text, font=font, fill=text_color)
        
        return image
    
    def get_unique_image(self, with_text=None):
        """Ottieni immagine unica"""
        # 50% random API, 50% generated
        if random.random() < 0.5:
            img = self.fetch_random_image()
            if img:
                img = img.resize((800, 600))
        else:
            img = self.generate_abstract_image()
        
        if not img:
            img = self.generate_abstract_image()
        
        if with_text:
            img = self.add_text_to_image(img, with_text)
        
        # Salva in memoria
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=90)
        img_bytes.seek(0)
        
        return img_bytes

# ==================== USAGE ====================
img_gen = FreeImageGenerator()
image_data = img_gen.get_unique_image(with_text="JOIN DISCORD")
