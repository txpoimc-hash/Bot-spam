#!/usr/bin/env python3
# ultimate_free_promoter_render.py
# Versione definitiva: multi-piattaforma + multi-account illimitati

import os
import sys
import time
import random
import json
import logging
from datetime import datetime
from pyvirtualdisplay import Display
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup

# I tuoi moduli personali
from proxy_free_collector import FreeProxyCollector
from user_agent_manager import UserAgentManager
from email_generator_free import FreeEmailGenerator
from image_generator_free import FreeImageGenerator
from content_spinner_free import FreeContentSpinner
from notifications_free import FreeNotifier
from captcha_solver_free import FreeCaptchaSolver

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UltimatePromoBot:
    """Bot multi-piattaforma con gestione infinita di account"""

    def __init__(self):
        logger.info("🚀 Avvio Ultimate Promo Bot 2026")

        # Schermo virtuale per headless
        self.display = Display(visible=0, size=(1920, 1080))
        self.display.start()

        # Moduli di supporto
        self.proxy_manager = FreeProxyCollector()
        self.ua_manager = UserAgentManager()
        self.email_gen = FreeEmailGenerator()
        self.img_gen = FreeImageGenerator()
        self.spinner = FreeContentSpinner()
        self.notifier = FreeNotifier()
        self.captcha_solver = FreeCaptchaSolver()

        # Carica configurazioni
        self.config = self.load_config()
        self.accounts = self.load_accounts()          # tutti gli account per piattaforma
        self.stats = self.load_stats()
        self.targets = self.load_targets()            # gruppi / subreddit / canali

        # Pool proxy iniziale
        self.refresh_proxies()

        # Contatori per rotazione account
        self.account_index = {platform: 0 for platform in self.config['platforms']}

        logger.info("✅ Inizializzazione completata")

    # ------------------------------------------------------------------
    # CARICAMENTO CONFIGURAZIONI
    # ------------------------------------------------------------------
    def load_config(self):
        """Carica configurazione generale"""
        default_config = {
            'platforms': [
                'facebook', 'reddit', 'telegram', 'discord',
                'quora', 'medium', 'linkedin', 'twitter',
                'pinterest', 'tumblr', 'forum'
            ],
            'max_posts_per_day': 100,
            'min_delay': 1800,      # 30 min
            'max_delay': 7200,      # 2 ore
            'headless': True,
            'use_proxy': True,
            'use_images': True,
            'use_captcha_solver': False,
            'accounts_file': 'accounts.json',
            'targets_file': 'target_groups.json'
        }
        # Se esiste un file di configurazione esterno, caricalo
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        return default_config

    def load_accounts(self):
        """Carica tutti gli account da accounts.json"""
        if os.path.exists(self.config['accounts_file']):
            with open(self.config['accounts_file'], 'r') as f:
                return json.load(f)
        else:
            # Crea file vuoto con struttura di esempio
            template = {
                "facebook": [],
                "reddit": [],
                "telegram": [],
                "discord": [],
                "quora": [],
                "medium": [],
                "linkedin": [],
                "twitter": [],
                "pinterest": [],
                "tumblr": [],
                "forum": []
            }
            with open(self.config['accounts_file'], 'w') as f:
                json.dump(template, f, indent=2)
            return template

    def load_targets(self):
        """Carica i target (gruppi, subreddit, ecc.)"""
        if os.path.exists(self.config['targets_file']):
            with open(self.config['targets_file'], 'r') as f:
                return json.load(f)
        else:
            # Crea template vuoto
            template = {
                "facebook": [],
                "reddit": [],
                "telegram": [],
                "discord": [],
                "quora": [],
                "medium": [],
                "linkedin": [],
                "twitter": [],
                "pinterest": [],
                "tumblr": [],
                "forum": []
            }
            with open(self.config['targets_file'], 'w') as f:
                json.dump(template, f, indent=2)
            return template

    def load_stats(self):
        if os.path.exists('stats.json'):
            with open('stats.json', 'r') as f:
                return json.load(f)
        return {
            'total_posts': 0,
            'successful_posts': 0,
            'failed_posts': 0,
            'banned_accounts': 0,
            'last_run': None,
            'daily_stats': {}
        }

    def save_stats(self):
        with open('stats.json', 'w') as f:
            json.dump(self.stats, f, indent=2)

    def refresh_proxies(self):
        """Aggiorna la lista di proxy funzionanti"""
        logger.info("🔄 Aggiornamento proxy...")
        self.proxy_manager.collect_all_proxies()
        self.working_proxies = self.proxy_manager.test_proxies_parallel(max_workers=20)
        logger.info(f"✅ {len(self.working_proxies)} proxy funzionanti")
        # Salva su file
        with open('working_proxies.txt', 'w') as f:
            for proxy in self.working_proxies[:100]:
                f.write(f"{proxy}\n")

    # ------------------------------------------------------------------
    # GESTIONE ACCOUNT (ROUND-ROBIN)
    # ------------------------------------------------------------------
    def get_next_account(self, platform):
        """Restituisce il prossimo account disponibile per la piattaforma (round-robin)"""
        accounts = self.accounts.get(platform, [])
        if not accounts:
            return None
        # Filtra solo account attivi
        active = [a for a in accounts if a.get('status') == 'active']
        if not active:
            return None
        # Usa indice round-robin
        idx = self.account_index.get(platform, 0) % len(active)
        self.account_index[platform] = idx + 1
        return active[idx]

    def mark_account_banned(self, platform, account):
        """Segna un account come bannato"""
        for acc in self.accounts[platform]:
            if acc['email'] == account['email']:
                acc['status'] = 'banned'
                self.stats['banned_accounts'] += 1
                logger.warning(f"⚠️ Account bannato: {account['email']}")
                break
        self.save_accounts()

    def save_accounts(self):
        """Salva lo stato aggiornato degli account"""
        with open(self.config['accounts_file'], 'w') as f:
            json.dump(self.accounts, f, indent=2)

    # ------------------------------------------------------------------
    # CREAZIONE DRIVER SELENIUM (CON PROXY E USER-AGENT)
    # ------------------------------------------------------------------
    def create_driver(self, platform=None):
        """Crea un driver Chrome con proxy e user-agent casuali"""
        options = uc.ChromeOptions()
        if self.config['headless']:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # User-agent casuale
        if platform:
            ua = self.ua_manager.get_ua_with_platform(platform)
        else:
            ua = self.ua_manager.get_random_ua()
        options.add_argument(f'user-agent={ua}')

        # Proxy se abilitato
        if self.config['use_proxy'] and self.working_proxies:
            proxy = random.choice(self.working_proxies)
            options.add_argument(f'--proxy-server=http://{proxy}')
            logger.debug(f"🔌 Usando proxy: {proxy}")

        # Dimensioni finestra casuali
        width = random.randint(1200, 1920)
        height = random.randint(800, 1080)
        options.add_argument(f'--window-size={width},{height}')

        try:
            driver = uc.Chrome(options=options, version_main=122)
            # Anti-detection aggiuntivo
            driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            """)
            return driver
        except Exception as e:
            logger.error(f"❌ Errore creazione driver: {e}")
            return None

    # ------------------------------------------------------------------
    # METODI PER OGNI PIATTAFORMA
    # ------------------------------------------------------------------

    # ---------- FACEBOOK (gruppi) ----------
    def post_to_facebook(self):
        """Post automatico nei gruppi Facebook"""
        platform = 'facebook'
        account = self.get_next_account(platform)
        if not account:
            logger.warning("⚠️ Nessun account Facebook disponibile")
            return

        groups = self.targets.get(platform, [])
        if not groups:
            logger.warning("⚠️ Nessun gruppo Facebook configurato")
            return

        driver = self.create_driver(platform='windows')
        if not driver:
            return

        try:
            # Login
            driver.get("https://www.facebook.com/")
            wait = WebDriverWait(driver, 30)
            email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
            email_field.send_keys(account['email'])
            password_field = driver.find_element(By.ID, "pass")
            password_field.send_keys(account['password'])
            password_field.send_keys(Keys.RETURN)
            time.sleep(random.uniform(5, 10))

            # Verifica login
            if "checkpoint" in driver.current_url or "login" in driver.current_url:
                logger.error("❌ Login Facebook fallito (2FA o credenziali errate)")
                self.mark_account_banned(platform, account)
                driver.quit()
                return

            # Posta in alcuni gruppi (max 3 per sessione)
            posted = 0
            for group_url in random.sample(groups, min(3, len(groups))):
                try:
                    driver.get(group_url)
                    time.sleep(random.uniform(4, 8))

                    # Crea messaggio variato
                    base = "Join our awesome community! Discord & Telegram links inside."
                    message = self.spinner.generate_post_variation(base, 'discord', 'gaming')
                    if self.config['use_images']:
                        image_data = self.img_gen.get_unique_image(with_text="JOIN US")
                        # Qui dovresti implementare l'upload dell'immagine (non trivial)
                        # Per semplicità, postiamo solo testo

                    # Trova box di testo
                    post_box = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//div[@role='textbox'] | //div[contains(@aria-label, 'Write something')]")
                    ))
                    post_box.click()
                    time.sleep(1)
                    post_box.send_keys(message)
                    time.sleep(random.uniform(2, 4))

                    # Pubblica
                    post_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Post' or contains(text(), 'Post')]")
                    if post_buttons:
                        driver.execute_script("arguments[0].scrollIntoView(true);", post_buttons[-1])
                        time.sleep(1)
                        post_buttons[-1].click()
                        time.sleep(random.uniform(5, 10))
                        posted += 1
                        self.stats['successful_posts'] += 1
                        logger.info(f"✅ Post Facebook in {group_url}")

                        # Delay casuale tra post
                        time.sleep(random.randint(600, 1800))  # 10-30 min
                except Exception as e:
                    logger.error(f"❌ Errore durante post in {group_url}: {e}")
                    self.stats['failed_posts'] += 1

            self.stats['total_posts'] += posted
            account['posts'] = account.get('posts', 0) + posted
            self.save_accounts()

        except Exception as e:
            logger.error(f"❌ Errore generale Facebook: {e}")
        finally:
            driver.quit()

    # ---------- REDDIT (subreddit) ----------
    def post_to_reddit(self):
        """Post automatico su Reddit"""
        platform = 'reddit'
        account = self.get_next_account(platform)
        if not account:
            logger.warning("⚠️ Nessun account Reddit")
            return

        subreddits = self.targets.get(platform, [])
        if not subreddits:
            logger.warning("⚠️ Nessun subreddit configurato")
            return

        driver = self.create_driver(platform='windows')
        if not driver:
            return

        try:
            # Login
            driver.get("https://www.reddit.com/login/")
            wait = WebDriverWait(driver, 30)
            user_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            user_field.send_keys(account['username'])
            pass_field = driver.find_element(By.NAME, "password")
            pass_field.send_keys(account['password'])
            pass_field.send_keys(Keys.RETURN)
            time.sleep(random.uniform(5, 10))

            # Post in alcuni subreddit
            for sub in random.sample(subreddits, min(2, len(subreddits))):
                try:
                    driver.get(f"https://www.reddit.com{sub}/submit")
                    time.sleep(3)

                    # Titolo
                    title_field = wait.until(EC.presence_of_element_located((By.NAME, "title")))
                    title = self.spinner.generate_post_variation("Join our Discord!", 'reddit', 'gaming')
                    title_field.send_keys(title)

                    # Contenuto (testo)
                    content = self.spinner.generate_post_variation("We have daily giveaways and events!", 'reddit', 'gaming')
                    text_area = driver.find_element(By.XPATH, "//textarea | //div[@role='textbox']")
                    text_area.click()
                    text_area.send_keys(content)

                    # Invia
                    submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Post')]")
                    submit_btn.click()
                    time.sleep(5)
                    logger.info(f"✅ Post Reddit in {sub}")
                    self.stats['successful_posts'] += 1
                    self.stats['total_posts'] += 1
                    account['posts'] += 1

                    time.sleep(random.randint(1200, 3600))  # 20-60 min
                except Exception as e:
                    logger.error(f"❌ Errore su {sub}: {e}")
                    self.stats['failed_posts'] += 1

            self.save_accounts()
        except Exception as e:
            logger.error(f"❌ Errore Reddit: {e}")
        finally:
            driver.quit()

    # ---------- TELEGRAM (gruppi) ----------
    def post_to_telegram(self):
        """Post su gruppi Telegram (via web version)"""
        platform = 'telegram'
        account = self.get_next_account(platform)
        if not account:
            logger.warning("⚠️ Nessun account Telegram")
            return

        groups = self.targets.get(platform, [])
        if not groups:
            logger.warning("⚠️ Nessun gruppo Telegram configurato")
            return

        # Per Telegram serve il numero di telefono (account['phone'])
        driver = self.create_driver(platform='mobile')
        if not driver:
            return

        try:
            # Login su web.telegram.org
            driver.get("https://web.telegram.org/k/")
            wait = WebDriverWait(driver, 30)
            # Inserisci numero (potrebbe essere complicato, usiamo un approccio semplificato)
            # ... (omettiamo per brevità, ma si può implementare)
            logger.info("⚠️ Telegram login non ancora implementato (servirebbe gestione sessioni)")
            # Se hai già i cookie, puoi caricarli
            time.sleep(5)
        except Exception as e:
            logger.error(f"❌ Telegram: {e}")
        finally:
            driver.quit()

    # ---------- DISCORD (server) ----------
    def post_to_discord(self):
        """Post su canali Discord (via browser)"""
        platform = 'discord'
        account = self.get_next_account(platform)
        if not account:
            logger.warning("⚠️ Nessun account Discord")
            return

        servers = self.targets.get(platform, [])
        if not servers:
            logger.warning("⚠️ Nessun server Discord configurato")
            return

        driver = self.create_driver(platform='windows')
        if not driver:
            return

        try:
            # Login Discord (potrebbe richiedere token)
            driver.get("https://discord.com/login")
            wait = WebDriverWait(driver, 30)
            # Login via token (più semplice)
            driver.execute_script(f"""
                function login(token) {{
                    setInterval(() => {{
                        document.body.appendChild(document.createElement`iframe`).contentWindow.localStorage.token = `"${{token}}"`;
                    }}, 50);
                    setTimeout(() => {{ location.reload(); }}, 2500);
                }}
                login('{account['token']}');
            """)
            time.sleep(5)

            # Per ogni server, apri un canale e posta
            for server_invite in servers:
                driver.get(server_invite)
                time.sleep(5)
                # Cerca textarea e scrivi
                try:
                    msg_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']")))
                    msg_box.click()
                    msg = self.spinner.generate_post_variation("Join our community!", 'discord', 'gaming')
                    msg_box.send_keys(msg)
                    msg_box.send_keys(Keys.RETURN)
                    time.sleep(3)
                    logger.info(f"✅ Post Discord in {server_invite}")
                    self.stats['successful_posts'] += 1
                except:
                    pass
        except Exception as e:
            logger.error(f"❌ Discord: {e}")
        finally:
            driver.quit()

    # ---------- QUORA (spazi) ----------
    def post_to_quora(self):
        """Risponde a domande o pubblica su Spazi"""
        platform = 'quora'
        account = self.get_next_account(platform)
        if not account:
            return
        # ... implementazione simile con Selenium
        logger.info("⚠️ Quora non implementato, stub")

    # ---------- MEDIUM ----------
    def post_to_medium(self):
        """Pubblica articoli su Medium"""
        platform = 'medium'
        account = self.get_next_account(platform)
        if not account:
            return
        # ...
        logger.info("⚠️ Medium non implementato, stub")

    # ---------- LINKEDIN (gruppi) ----------
    def post_to_linkedin(self):
        """Post su gruppi LinkedIn"""
        platform = 'linkedin'
        account = self.get_next_account(platform)
        if not account:
            return
        # ...
        logger.info("⚠️ LinkedIn non implementato, stub")

    # ---------- TWITTER (X) ----------
    def post_to_twitter(self):
        """Tweet con hashtag"""
        platform = 'twitter'
        account = self.get_next_account(platform)
        if not account:
            return
        driver = self.create_driver(platform='mobile')
        # ...
        logger.info("⚠️ Twitter non implementato, stub")

    # ---------- PINTEREST ----------
    def post_to_pinterest(self):
        """Pin su bacheche"""
        platform = 'pinterest'
        account = self.get_next_account(platform)
        if not account:
            return
        # ...
        logger.info("⚠️ Pinterest non implementato, stub")

    # ---------- TUMBLR ----------
    def post_to_tumblr(self):
        """Post su blog Tumblr"""
        platform = 'tumblr'
        account = self.get_next_account(platform)
        if not account:
            return
        # ...
        logger.info("⚠️ Tumblr non implementato, stub")

    # ---------- FORUM (vBulletin, phpBB) ----------
    def post_to_forum(self):
        """Post su forum generici (configurabili)"""
        platform = 'forum'
        account = self.get_next_account(platform)
        if not account:
            return
        forums = self.targets.get(platform, [])
        if not forums:
            return
        driver = self.create_driver(platform='windows')
        # ...
        logger.info("⚠️ Forum generico non implementato, stub")

    # ------------------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------------------
    def run(self):
        """Ciclo principale: esegue tutte le piattaforme a rotazione"""
        logger.info("🎯 Avvio ciclo principale")

        while True:
            # Mescola l'ordine delle piattaforme
            platforms = self.config['platforms'].copy()
            random.shuffle(platforms)

            for platform in platforms:
                logger.info(f"--- Inizio campagna {platform.upper()} ---")
                try:
                    # Chiama il metodo corrispondente
                    method_name = f"post_to_{platform}"
                    if hasattr(self, method_name):
                        method = getattr(self, method_name)
                        method()
                    else:
                        logger.warning(f"⚠️ Metodo {method_name} non implementato")
                except Exception as e:
                    logger.error(f"❌ Errore in {platform}: {e}")

                # Pausa tra piattaforme
                pause = random.randint(1800, 3600)  # 30-60 min
                logger.info(f"⏳ Pausa di {pause/60:.1f} minuti prima della prossima piattaforma")
                time.sleep(pause)

                # Rinfresca proxy ogni 3 piattaforme
                if random.randint(1, 3) == 1:
                    self.refresh_proxies()

            # Fine ciclo completo
            self.stats['last_run'] = datetime.now().isoformat()
            self.save_stats()

            # Notifica
            self.notifier.send_stats({
                'posts': self.stats['successful_posts'],
                'success': self.stats['successful_posts'],
                'fails': self.stats['failed_posts'],
                'bans': self.stats['banned_accounts'],
                'rate': (self.stats['successful_posts'] / max(self.stats['total_posts'], 1)) * 100
            })

            # Pausa lunga tra cicli
            cycle_delay = random.randint(14400, 43200)  # 4-12 ore
            logger.info(f"✅ Ciclo completato. Prossimo tra {cycle_delay/3600:.1f} ore")
            time.sleep(cycle_delay)

    def cleanup(self):
        self.display.stop()
        logger.info("🧹 Cleanup eseguito")

if __name__ == "__main__":
    bot = UltimatePromoBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("👋 Interrotto dall'utente")
    finally:
        bot.cleanup()
